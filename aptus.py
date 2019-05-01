#local modules
import cookiehandler
import card

from werkzeug.exceptions import Unauthorized, HTTPException, NotFound
import lxml.html
import requests
import json
import re



session = requests.Session()

## controls how many minutes before a cookie expires. Can be changed
## aspx cookies seem to only work for 5 minutes. chs cookies work longer
cookie_duration = 5
## dict to store instances of CookieHandler class
user_cookies = dict()



############################## Helper functions ##############################

## handles login and sets cookies in user_cookies dict.
## description is for specifying if you want cookies for apt-chalmersstudentbostader.se (aspx) or just chalmersstudentbostader.se (chs)
def handle_login(user, pwd, description):
    # lazy eval makes this condition work
    if(not user in user_cookies or not user_cookies[user].get_cookies()):
        
        # init cookihandler for user
        user_cookies[user] = cookiehandler.CookieHandler(cookie_duration)
        # login to mina sidor. Store cookies
        chs_cookies = chs_login(user, pwd).cookies
        user_cookies[user].add_cookie({ "chs" :  chs_cookies})
        
        # if we need aspx cookies (laundry or lock). e.g invoices and contact info does not need this
        need_aspx = True if description in {"laundry", "lock"} else False

        if(need_aspx):
            # get lock or laundry url
            aspx_url = get_aptus_url(user, need_aspx and description == "laundry")
            # goto aspx_url. Store cookies
            aspx_cookies = session.get(aspx_url).cookies
            user_cookies[user].add_cookie({ "aspx": aspx_cookies })


## Attempts to log in to chs mina sidor
def chs_login(user, pwd):
    login_response = session.post("https://www.chalmersstudentbostader.se/wp-login.php", data = {"log" : user, "pwd" : pwd})
    
    #login error
    #raise httpexception instead?
    if login_response.url[-9:] == "err=login": 
         raise Unauthorized("There was an error logging in. This is most likely due to an incorrect username or password")
    return login_response



## returns the URL for aptusport or laundry services. sel - True/False
## return format:
##     <baseURL>?module=<Lock|Booking>&customerName=<Customer>&timestamp=<Timestamp>&hash=<Hash>
def get_aptus_url(user, sel):
    aptus_response = session.get("https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=aptuslogin@APTUSPORT&widgets[]=aptuslogin", 
        cookies=user_cookies[user].get_cookies()["chs"])

    aptus_json = json.loads(aptus_response.text[2:-2])

    if(not aptus_json["data"]):
        raise HTTPException("Error in get_aptus_url(). Could not fetch aptus URL (aptuslogin)")

    # selects Aptusport URL or Laundry URL.
    widget_url = "aptuslogin@APTUSPORT" if bool(sel) else "aptuslogin"
    return json.loads(str(aptus_json["data"][widget_url]["objekt"][0]).replace('\'',"\""))["aptusUrl"]



############################## Handles flask requests (from app.py) ##############################

## given credentials and door, opens it
def unlock_door(user, pwd, door_name):
    handle_login(user, pwd, "lock")

    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/Lock/UnlockEntryDoor/" + door_name,
        cookies=user_cookies[user].get_cookies()["aspx"])
    
    open_res = json.loads(res.text)
    if(not open_res["StatusText"]):
        raise HTTPException("Error in unlock_door(). Could not open the door")

    return {
        "status" : "success",
        "data" : {
            "id" : door_name,
            "message" : open_res["StatusText"]
        }
    }



def get_available_doors(user, pwd):
    handle_login(user, pwd, "lock")

    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/Lock", 
        cookies=user_cookies[user].get_cookies()["aspx"])
    return card.Card(res.content, 0, "door", "door_id").get_card()



## fetches users currently booked laundry passes
def get_laundry_bookings(user, pwd):
    handle_login(user, pwd, "laundry")

    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/CustomerBooking", 
        cookies=user_cookies[user].get_cookies()["aspx"])
    return card.Card(res.content, 1, "time", "duration", "day", "machines", "street", "machine_id").get_card()



## returns closest available passes for booking
def get_available_machines(user, pwd, num):
    handle_login(user, pwd, "laundry")

    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/CustomerBooking/FirstAvailable?categoryId=1&firstX=" + num, 
        cookies=user_cookies[user].get_cookies()["aspx"])
    return card.Card(res.content, 2, "time", "date", "laundry_room", "street", "booking_params").get_card()



## books a machine
def book_machine(user, pwd, booking_group_no, pass_no, pass_date):
    handle_login(user, pwd, "laundry")

    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/CustomerBooking/Book?passNo="+pass_no+"&passDate="+pass_date+"&bookingGroupId="+booking_group_no, 
        cookies=user_cookies[user].get_cookies()["aspx"])
    # scrape result of booking machine
    return card.Card(res.content, 4, "booking_result").get_card()



# cancels laundry pass 
def unbook_machine(user, pwd, machine_id):
    handle_login(user, pwd, "laundry")

    res = session.get("https://apt-www.chalmersstudentbostader.se/AptusPortal/CustomerBooking/Unbook/" + machine_id, 
        cookies=user_cookies[user].get_cookies()["aspx"])
    #scrape result of unbooking machine
    return card.Card(res.content, 4, "unbooking_result").get_card()



# returns sum of paid, pending and unpaid invoices
def get_invoice_sum(user, pwd):
    handle_login(user, pwd, "chs")

    res = session.get("https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=avisummering", 
        cookies=user_cookies[user].get_cookies()["chs"])
    
    # invoice sum returned in JSON so we do not need to scrape this either.
    invoice_sum_json = json.loads(res.content[2:-2])["data"]
    if (not invoice_sum_json["avisummering"]):
        raise HTTPException("Error in get_invoice_sum(). Could not fetch invoice sum (avisummering)")

    return { "data" : invoice_sum_json, "status": "success"}



# returns a detailed list of invoices, amounts, status of payment, when to pay etc
def get_invoice_list(user, pwd):
    handle_login(user, pwd, "chs")

    res = session.get("https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=avilista", 
        cookies=user_cookies[user].get_cookies()["chs"])

    # invoice data embedded in HTML so we must scrape it with Card class
    avilista_html = json.loads(res.content[2:-2])["html"]["avilista"]
    return card.Card(avilista_html, 3, "invoice", "invoice_status", "amount", "date_of_payment", "ocr", "pdf_link").get_card()



# returns contact info for user
def get_contact_info(user, pwd):
    handle_login(user, pwd, "chs")

    res = session.get("https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=kontaktuppgifter", 
        cookies=user_cookies[user].get_cookies()["chs"])

    # contact info returned in JSON so we do not need to scrape it.
    contact_json = json.loads(res.content[2:-2])["data"]
    if(not contact_json["kontaktuppgifter"]):
        raise HTTPException("Error in get_contact_info(). Could not fetch contact info (kontaktuppgifter)")

    return {"data" : contact_json, "status" : "success"}


# Retrieves the latest news from chalmers studentbostäder
def get_news(news_category):
    if(news_category in {"nyheter", "omradesnyhet"}):
        news_page_html = session.get("https://www.chalmersstudentbostader.se/nyheter/kategori/" + news_category)
    else:
        raise NotFound("not a valid address for news (nyheter/omradesnyhet)")

    return card.Card(news_page_html.content, 5, "news_date", "news_headline", "news_text", "news_link").get_card()