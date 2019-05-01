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
        xpath_result = ""

        ## Scrape info from HTML page
        for arg in argv:
            temp[arg] = ""
            xpath_result = ""

            #### Laundry (Schedule and available passes) ####
            if(arg == "time"):
                xpath_result = card.xpath(".//div[1]/text()")

            elif(arg == "day"):
                xpath_result = card.xpath(".//div[2]/text()")

            elif(arg == "date"):
                xpath_result = card.xpath(".//div[2]/text()")

            elif(arg == "street"):
                xpath_result = card.xpath(".//div[5]/text()")

            elif(arg == "duration"):
                xpath_result = card.xpath(".//div[1]/text()")

            elif(arg == "machines"):
                xpath_result = card.xpath(".//div[4]/text()")

            elif(arg == "machine_id"):
                xpath_result = int(card.xpath(".//button/@id")[0])

            elif(arg == "laundry_room"):
                xpath_result = card.xpath(".//div[4]/text()")

            #### Available doors ####
            elif(arg == "door"):
                xpath_result = card.xpath(".//div/span/text()")

            elif(arg == "door_id"):
                # extracts door id from function call. Ex UnlockEntranceDoor(123456) returns 123456
                rgx_door_id = re.search(r"\(([^)]+)\)",card.xpath(".//button/@onclick")[0]).group(1)
                xpath_result = int(rgx_door_id)
            
            #### Invoice ####
            elif(arg == "invoice"):
                xpath_result = card.xpath(".//div[1]/h4/text()")

            elif(arg == "invoice_status"):
                # sometimes the card contains multiple <span> tags so we join them together
                xpath_result =  "".join(card.xpath(".//div[2]/div/span/text()"))

            elif(arg == "amount"):
                xpath_result = card.xpath(".//dl[1]/dd/text()")

            elif(arg == "date_of_payment"):
                xpath_result = card.xpath(".//dl[2]/dd/text()")

            elif(arg == "ocr"):
                xpath_result = int(card.xpath(".//dl[3]/dd/text()")[0])

            elif(arg == "pdf_link"):
                xpath_result = card.xpath(".//div[3]/a/@href")

            #### booking/cancel result ####
            elif(arg in {"booking_result", "unbooking_result"}):
                xpath_result = re.search(r"(?<=FeedbackDialog\(\').[^']*", card.xpath(".//text()")[0]).group()

            #### News ####
            elif(arg == "news_date"):
                xpath_result = card.xpath(".//span[@class=\"Date\"]/text()")

            elif(arg == "news_headline"):
                xpath_result = card.xpath(".//header[@class=\"Header\"]/h2/a/text()")
            
            elif(arg == "news_link"):
                xpath_result = card.xpath(".//header[@class=\"Header\"]/h2/a/@href")
    
            elif(arg == "news_text"):
                xpath_result = card.xpath(".//p/text()")

            #### Booking pass related data ####
            # needed for /laundry/book
            # extracted from url parameter. 
            # Ex: passNo=xx, bookingGroupId=xx, passDate=yyyy-mm-dd
            elif(arg == "booking_params"):
                temp[arg] = {}
                misc = card.xpath(".//button/@onclick")[0][10:-17]
                for misc_item in re.findall(r"(\?|\&)([^=]+)\=([^&]+)",misc):
                    temp[arg][misc_item[1]] = misc_item[2]

            if(arg != "booking_params"):
                if(isinstance(xpath_result, list)):
                    temp[arg] = xpath_result[0].strip()
                else:
                    temp[arg] = xpath_result


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
                booking_cards = html_obj.xpath(".//div[contains(@class, \"lockCard\")]")
            elif(sel == 1):
                booking_cards = html_obj.xpath(".//div[@id=\"newBookingCard\"]/following-sibling::div[@class=\"bookingCard\"]")
            elif(sel == 2):
                booking_cards = html_obj.xpath(".//div[@class=\"bookingCard\"]")
            elif(sel == 3):
                booking_cards = html_obj.xpath(".//div[contains(@class,\"AviListItem\")]//div[@class=\"span6\"]/..")
            elif(sel == 4):
                booking_cards = html_obj.xpath(".//script[contains(text(), \"FeedbackDialog\")]")
            elif(sel == 5):
                booking_cards = html_obj.xpath(".//article[@class=\"ArchiveItem\"]")

            #xpath empty means something went wrong (except for laundry passes)
            if(not booking_cards and sel is not 1):
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