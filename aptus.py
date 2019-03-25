import lxml.html
import requests
import json
import re

with open("doors.json") as file:
    available_doors = json.load(file)

session = requests.Session()
base_url = "https://apt-www.chalmersstudentbostader.se/"

## helper function, returns the URL for aptusport or laundry services
## return format: <baseURL>?module=<Lock|Booking>&customerName=<Customer>&timestamp=<Timestamp>&hash=<Hash>
def getAptusUrl(user, pwd, sel):
    check_login = session.post("https://www.chalmersstudentbostader.se/wp-login.php", data = {"log" : user, "pwd" : pwd})
    
    # not fault redundant
    # move error handling
    if(check_login.url[-9:] == "err=login"):
        return "There was an error logging in. This is most likely due to an incorrect username or password"

    r = session.get("https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=aptuslogin@APTUSPORT&widgets[]=aptuslogin")
    s = json.loads(r.text[2:-2])

    # decides between aptusport or laundry services
    which_aptus = "aptuslogin@APTUSPORT" if bool(sel) else "aptuslogin"
    return json.loads(str(s["data"][which_aptus]["objekt"][0]).replace('\'',"\""))["aptusUrl"]

## given credentials and door, opens it    
def unlockDoor(user, pwd, door_name):
    unlock_url = getAptusUrl(user, pwd, True)
    session.get(unlock_url)
    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/Lock/UnlockEntryDoor/" + available_doors[door_name])
    return {
        "door" : {
            "doorName" : door_name,
            "doorId" : available_doors[door_name]
        },
        "aptus_response" : json.loads(res.text)
    }

## fetches users currently booked laundry passes
def getLaundryBookings(user, pwd):
    laundry_url = getAptusUrl(user, pwd, False)
    res = session.get(laundry_url)
    booking_cards = lxml.html.fromstring(res.content).xpath("/html/body/div/section/div[1]/div[1]/div[position()>1]")
    
    ## TODO: remove whitespace and newline characters
    laundry_schedule = []
    for card in booking_cards:
        temp = {}
        temp["timestamp"] = card.xpath(".//button/@aria-label")[13:]     
        temp["duration"] = card.xpath(".//div[1]/text()")
        temp["day"] = card.xpath(".//div[2]/text()")
        temp["machines"] = card.xpath(".//div[4]/text()")
        temp["machines"]["id"] = card.xpath("")
        temp["street"] = card.xpath(".//div[5]/text()")
        laundry_schedule.append(temp)
    return laundry_schedule

## returns closest available machines
def getAvailableMachines(user, pwd, num):
    laundry_url = getAptusUrl(user, pwd, False)
    session.get(laundry_url)
    
    res = session.get(base_url + "/AptusPortal/CustomerBooking/FirstAvailable?categoryId=1&firstX="+ (num or 10 ))
    booking_cards = lxml.html.fromstring(res.content).xpath("/html/body/div/section/div/div")

    ## TODO: remove whitespace and newline characters
    available_machines = []
    for card in booking_cards:
        temp = {}
        temp["time"] = card.xpath(".//div[1]/text()")
        temp["date"] = card.xpath(".//div[2]/text()")
        temp["laundry room"] = card.xpath(".//div[4]/text()")
        temp["street"] = card.xpath(".//div[5]/text()")
        
        # misc info needed to book, located in URL string
        # regex parses out parameters
        misc = card.xpath(".//button/@onclick")[0][10:-16]
        for misc_item in re.findall(r"(\?|\&)([^=]+)\=([^&]+)",misc):
            temp[misc_item[1]] = misc_item[2]

        available_machines.append(temp)
    return available_machines

## books a machine
def bookMachine(user, pwd, bookingGrpNo, passNo, passDate):
    laundry_url = getAptusUrl(user, pwd, False)
    session.get(laundry_url)
    res = session.get(base_url + "/AptusPortal/CustomerBooking/BookFirstAvailable?"+
        "passNo="+passNo+"&passDate="+passDate+"&bookingGroupId="+bookingGrpNo)

    return 0