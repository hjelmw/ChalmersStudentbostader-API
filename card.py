import lxml.html
import re

## This class parses an HTML document, returning a dict with the info requested.
##
## arguments: 
##    HTML_OBJ - HTML document
##    sel - specify which page you gave the constructor (True for active bookings, False for available machines)
##    *argv - what do you want returned in the dict ex Card(.., .., "timestamp", "machine_id", "building")
##
## getCard returns:
##    dict of the following format:
##    {
##    "data" : {...},
##    "status" : success/error,
##    }
class Card:
    card_obj = dict()


    def __parse_card(self, card, i, sel, argv):
        
        # init temp dict. Will append to card_obj later
        temp = {}

        ## Scrape info from HTML page
        for arg in argv:

            #### Laundry (Schedule and available passes) ####
            if(arg == "time"):
                temp["time"] = card.xpath(".//div[1]/text()")[0][18:-14]

            elif(arg == "day"):
                temp["day"] = card.xpath(".//div[2]/text()")[0][22:-18]

            elif(arg == "date"):
                temp["date"] = card.xpath(".//div[2]/text()")[0][18:-14]

            elif(arg == "street"):
                index = 22 if sel == 1 else 18
                temp["street"] = card.xpath(".//div[5]/text()")[0][index:]

            elif(arg == "duration"):
                temp["duration"] = card.xpath(".//div[1]/text()")[0][22:-18]

            elif(arg == "machines"):
                temp["machines"] = card.xpath(".//div[4]/text()")[0][22:]

            elif(arg == "machine_id"):
                temp["machine_id"] = int(card.xpath(".//button/@id")[0])

            elif(arg == "laundry_room"):
                temp["laundry_room"] = card.xpath(".//div[4]/text()")[0][18:]

            #### Available doors ####
            elif(arg == "door"):
                temp["door"] = card.xpath(".//div/span/text()")[0]

            elif(arg == "door_id"):
                # extracts door id from function call. Ex UnlockEntranceDoor(123456) returns 123456
                rgx_door_id = re.search(r"\(([^)]+)\)",card.xpath(".//button/@onclick")[0]).group(1)
                temp["door_id"] = int(rgx_door_id)
            
            #### Invoice ####
            elif(arg == "invoice"):
                temp["invoice"] = card.xpath(".//div[1]/h4/text()")[0]

            elif(arg == "invoice_status"):
                # sometimes the card contains multiple <span> tags so we join them together
                temp["invoice_status"] =  "".join(card.xpath(".//div[2]/div/span/text()"))

            elif(arg == "amount"):
                temp["amount"] = card.xpath(".//dl[1]/dd/text()")[0]

            elif(arg == "date_of_payment"):
                temp["date_of_payment"] = card.xpath(".//dl[2]/dd/text()")[0]

            elif(arg == "ocr"):
                temp["ocr"] = int(card.xpath(".//dl[3]/dd/text()")[0])

            elif(arg == "pdf_link"):
                temp["pdf_link"] = card.xpath(".//div[3]/a/@href")[0]

            #### booking/cancel result ####
            elif(arg in {"booking_result", "unbooking_result"}):
                temp[arg] = re.search(r"(?<=FeedbackDialog\(\').[^']*", card.xpath(".//text()")[0]).group()
            
            #### News ####
            elif(arg == "news_date"):
                temp["news_date"] = card.xpath(".//span[@class=\"Date\"]/text()")[0]

            elif(arg == "news_headline"):
                temp["news_headline"] = card.xpath(".//header[@class=\"Header\"]/h2/a/text()")[0]
            
            elif(arg == "news_link"):
                temp["news_link"] = card.xpath(".//header[@class=\"Header\"]/h2/a/@href")[0]
    
            elif(arg == "news_text"):
                temp["news_text"] = card.xpath(".//p/text()")[0]          

            #### Booking pass related data ####
            # needed for /laundry/book
            # extracted from url parameter. 
            # Ex: passNo=xx, bookingGroupId=xx, passDate=yyyy-mm-dd
            elif(arg == "misc"):
                misc = card.xpath(".//button/@onclick")[0][10:-17]
                for misc_item in re.findall(r"(\?|\&)([^=]+)\=([^&]+)",misc):
                    temp[misc_item[1]] = misc_item[2]

        # add temp dict to return value
        self.card_obj["data"][i] = temp

    ## HTML_OBJ needs to be the HTML document for parsing to work
    ## args for parameters you want returned
    def __init__(self, HTML_OBJ, sel, *argv):        
        self.card_obj["data"] = {}

        # 0 - get_available_doors
        # 1 - get_laundry_bookings
        # 2 - get_available_machines
        # 3 - get_invoice_list
        # 4 - book_machine/unbook_machine
        # 5 - get_news
        try:
            html_obj = lxml.html.fromstring(HTML_OBJ)
            if(sel == 0):
                booking_cards = html_obj.xpath("/html/body/div/section/section/div[contains(@class, \"lockCard\")]")
            elif(sel == 1):
                booking_cards = html_obj.xpath("/html/body/div/section/div[1]/div[1]/div[position()>1]")
            elif(sel == 2):
                booking_cards = html_obj.xpath("/html/body/div/section/div/div")
            elif(sel == 3):
                booking_cards = html_obj.xpath(".//div[contains(@class,\"AviListItem\")]/div/div/div/div/div")
            elif(sel == 4):
                booking_cards = html_obj.xpath(".//script[contains(text(), \"FeedbackDialog\")]")
            elif(sel == 5):
                booking_cards = html_obj.xpath("/html/body/div[1]/div/div/div/div/div[@class=\"span9\"]/article")

            #xpath empty means something went wrong 
            if(not booking_cards):
                raise BookingCardParseException("xpath return empty. Check parameters")

            i = 0
            # extract arguments from HTML object and build dict
            for card in booking_cards:
                self.__parse_card(card, i, sel, argv) 
                i += 1
            self.card_obj["status"] = "success"
        
        except BookingCardParseException as e:
            self.card_obj = {"status": "error", "data" : {"message": "Error parsing a card", "details" : str(e), "parameters": {"sel": sel, "argv": argv}}}
        except Exception as e:
            self.card_obj = {"status": "error", "data" : {"message":"An unspecified error occured while parsing HTML object", "details" : str(e)}}
        
        
    def get_card(self):
        return self.card_obj


#Exception class to handle errors with booking/unbooking
class BookingCardParseException(Exception):
    pass