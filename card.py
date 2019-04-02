import lxml.html
import re

class Card:
    card_obj = []


    def __parseCard(self, card, sel, argv):

        temp = {}
        for arg in argv:

            if(arg == "time"):
                temp["time"] = card.xpath(".//div[1]/text()")[0][18:-14]

            elif(arg == "day"):
                temp["day"] = card.xpath(".//div[2]/text()")

            elif(arg == "date"):
                temp["date"] = card.xpath(".//div[2]/text()")[0][18:-14]

            elif(arg == "street"):
                temp["street"] = card.xpath(".//div[5]/text()")[0][18:]

            elif(arg == "duration"):
                temp["duration"] = card.xpath(".//div[1]/text()")

            elif(arg == "machines"):
                temp["machines"] = card.xpath(".//div[4]/text()")

            elif(arg == "machine_id"):
                temp["machine_id"] = card.xpath("")

            elif(arg == "laundry_room"):
                temp["laundry_room"] = card.xpath(".//div[4]/text()")[0][18:]

            # if /laundry/available
            elif(arg == "misc" and not sel):
                misc = card.xpath(".//button/@onclick")[0][10:-17]
                for misc_item in re.findall(r"(\?|\&)([^=]+)\=([^&]+)",misc):
                    temp[misc_item[1]] = misc_item[2]

        self.card_obj.append(temp)
        
    ## HTML_OBJ needs to be HTML object for aptus/module=Booking or /module=Lock 
    ## args for parameters you want returned
    def __init__(self, HTML_OBJ, sel, *argv):        
        self.card_obj = []

        # true getbooking false getavailable
        try:
            html_obj = lxml.html.fromstring(HTML_OBJ.content)
            if(sel):
                booking_cards = html_obj.xpath("/html/body/div/section/div[1]/div[1]/div[position()>1]")
            else:
                booking_cards = html_obj.xpath("/html/body/div/section/div/div")
            # extract arguments from HTML object
            for card in booking_cards:
                self.__parseCard(card, sel, argv)
            self.card_obj.append({"status": "success"})
        except Exception as e:
            self.card_obj = {"status": "error", "data" : {"message":"An error occured while parsing HTML object", "details" : str(e)}}


    def getCard(self):
        return self.card_obj
