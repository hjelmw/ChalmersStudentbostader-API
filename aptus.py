import lxml.html
import card
import requests
import json
import re

with open("doors.json") as file:
    available_doors = json.load(file)

session = requests.Session()


base_url =  "www.chalmersstudentbostader.se"


## maybe remove
def chsLogin(user, pwd):
    login_response = session.post("https://" + base_url + "/wp-login.php", data = {"log" : user, "pwd" : pwd})
    return "error" if login_response.url[-9:] == "err=login" else login_response



## helper function, returns the URL for aptusport or laundry services
## return format: <baseURL>?module=<Lock|Booking>&customerName=<Customer>&timestamp=<Timestamp>&hash=<Hash>
def getAptusUrl(user, pwd, sel):
    login_response = session.post("https://" + base_url + "/wp-login.php", data = {"log" : user, "pwd" : pwd})
    
    if(login_response.url[-9:] == "err=login"):
        return "error"

    r = session.get("https://" + base_url + "/widgets/?callback=?&widgets[]=aptuslogin@APTUSPORT&widgets[]=aptuslogin")
    s = json.loads(r.text[2:-2])

    # decides between aptusport or laundry services
    which_aptus = "aptuslogin@APTUSPORT" if bool(sel) else "aptuslogin"
    return json.loads(str(s["data"][which_aptus]["objekt"][0]).replace('\'',"\""))["aptusUrl"]



## given credentials and door, opens it    
def unlockDoor(user, pwd, door_name):
    unlock_url = getAptusUrl(user, pwd, True)
    if(unlock_url == "error"): 
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }

    session.get(unlock_url) 
    res = session.get("https://apt-" + base_url + "/AptusPortal/Lock/UnlockEntryDoor/" + door_name)
    return {
        "status" : "success",
        "data" : {
            "name" : door_name,
            "id" : available_doors[door_name],
            "aptus_response" : json.loads(res.text)
        }
    }



def getAvailableDoors(user, pwd):
    unlock_url = getAptusUrl(user, pwd, True)
    if(unlock_url == "error"): 
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }

    res = session.get(unlock_url)
    return card.Card(res.content, 0, "door", "door_id").getCard()
    


## fetches users currently booked laundry passes
def getLaundryBookings(user, pwd):
    laundry_url = getAptusUrl(user, pwd, False)
    if(laundry_url == "error"): 
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }
    
    res = session.get(laundry_url)
    #return card.Card(res, True, "timestamp", "duration", "day", "machines", "machine_id", "street").getCard()
    return card.Card(res.content, 1, "timestamp", "duration", "day", "machines", "street", "machine_id").getCard()



## returns closest available machines
def getAvailableMachines(user, pwd, num):
    laundry_url = getAptusUrl(user, pwd, False)
    if(laundry_url == "error"): 
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }
       
    session.get(laundry_url)
    res = session.get("https://apt-" + base_url + "/AptusPortal/CustomerBooking/FirstAvailable?categoryId=1&firstX=" + num)
    return card.Card(res.content, 2, "time","date", "laundry_room", "street", "misc").getCard()


def getInvoiceList(user, pwd):
    login_response = chsLogin(user, pwd)
    
    if(login_response == "error"):
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }

    res = session.get("https://" + base_url + "/widgets/?callback=?&widgets[]=avilista")
    
    avilista_html = json.loads(res.content[2:-2])["html"]["avilista"]

    # decides between aptusport or laundry services
    return card.Card(avilista_html, 3, "invoice", "invoice_status", "amount", "date_of_payment", "ocr", "pdf_link").getCard()


## books a machine
def bookMachine(user, pwd, bookingGrpNo, passNo, passDate):
    laundry_url = getAptusUrl(user, pwd, False)
    if(laundry_url == "error"): 
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }

    session.get(laundry_url)
    res = session.get("https://apt-" + base_url + "/AptusPortal/CustomerBooking/Book?" + "passNo="+passNo+"&passDate="+passDate+"&bookingGroupId="+bookingGrpNo)

    #scrape result of booking
    book_res = re.search(r"(?<=FeedbackDialog\(\').[^']*", lxml.html.fromstring(res.content).xpath("/html/body/div/section/script[contains(text(), \"FeedbackDialog\")]/text()")[0]).group()
    return {
            "status" : "success",
            "data" : {
                "message" : book_res
            }
        }

def unbookMachine(user, pwd, machine_id):
    laundry_url = getAptusUrl(user, pwd, False)
    if(laundry_url == "error"): 
        return {
            "status" : "failure",
            "data" : {
                "message" : "Could not authenticate against mina sidor. This is most likely due to an incorrect username or password."
            }
        }

    session.get(laundry_url)
    res = session.get("https://apt-" + base_url + "/AptusPortal/CustomerBooking/Unbook/" + str(machine_id))

    #scrape result of unbooking machine
    unbook_res = re.search(r"(?<=FeedbackDialog\(\').[^']*", lxml.html.fromstring(res.content).xpath("/html/body/div/section/script[contains(text(), \"FeedbackDialog\")]/text()")[0]).group()
    return {
            "status" : "success", 
            "data" : {
                "message" : unbook_res
            }
        }
