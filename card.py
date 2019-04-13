import lxml.html
import re

## This class parses an HTML document, returning a JSON-formatted string with the info requested.
##
## arguments: 
##    HTML_OBJ - HTML document
##    sel - specify which page you gave the constructor (True for active bookings, False for available machines)
##    *argv - what do you want returned in the JSON-string ex Card(.., .., "timestamp", "machine_id", "building")
##
## returns:
##    JSON-string of the following format:
##    {
##    "data" : {...},
##    "status" : success/error,
##    }
class Card:
    card_obj = []


    def __parseCard(self, card, sel, argv):

        temp = {}
        for arg in argv:
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
                temp["machine_id"] = card.xpath(".//button/@id")[0]

            elif(arg == "laundry_room"):
                temp["laundry_room"] = card.xpath(".//div[4]/text()")[0][18:]

            elif(arg == "door"):
                temp["door"] = card.xpath(".//div/span/text()")

            elif(arg == "door_id"):
                #rgx_id = re.findall(r"/\(([^)]+)\)/",card.xpath(".//button/@onclick"))
                temp["door_id"] = card.xpath(".//button/@onclick")

            # if /laundry/available
            elif(arg == "misc" and sel == 2):
                misc = card.xpath(".//button/@onclick")[0][10:-17]
                for misc_item in re.findall(r"(\?|\&)([^=]+)\=([^&]+)",misc):
                    temp[misc_item[1]] = misc_item[2]

        self.card_obj.append(temp)
        
    ## HTML_OBJ needs to be HTML object for aptus/module=Booking or /module=Lock 
    ## args for parameters you want returned
    def __init__(self, HTML_OBJ, sel, *argv):        
        self.card_obj = []

        # 0 - getAvailableDoors
        # 1 - getLaundryBookings
        # 2 - getAvailableMachines
        try:
            html_obj = lxml.html.fromstring(HTML_OBJ.content)
            if(sel == 0):
                booking_cards = html_obj.xpath("/html/body/div/section/section/div")
            elif(sel == 1):
                booking_cards = html_obj.xpath("/html/body/div/section/div[1]/div[1]/div[position()>1]")
            elif(sel == 2):
                booking_cards = html_obj.xpath("/html/body/div/section/div/div")
            
            # extract arguments from HTML object
            for card in booking_cards:
                self.__parseCard(card, sel, argv)
            self.card_obj.append({"status": "success"})
        except Exception as e:
            self.card_obj = {"status": "error", "data" : {"message":"An error occured while parsing HTML object", "details" : str(e)}}


    def getCard(self):
        return self.card_obj
