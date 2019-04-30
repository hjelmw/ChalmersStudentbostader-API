from flask import Flask, jsonify, request, redirect, url_for
#from flask_caching import Cache
from werkzeug.exceptions import HTTPException
import aptus
import json


app = Flask(__name__)

## simple for test/dev
## maybe redis for prod?
#cache = Cache(app, config = {"CACHE_TYPE" : "simple"})



## for Flask-Cache
## generates cache key based on user and password in form-data of request
def __make_cache_key(*args, **kwargs):
    args = str(hash(request.form["user"] + request.form["password"]))
    return (args).encode("utf-8")



############################# Error Routes #############################

## returns custom JSON for common error codes
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(status="error", code=code, error=str(e)), code



## for errorhandler
## Override default exception with custom JSON
from werkzeug.exceptions import default_exceptions
for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)



############################## API Routes ##############################

## opens one of the doors controlled by Aptusport
## params: 
##    user- username (chs mina sidor) 
##    password - password (chs mina sidor)
##    id of door to unlock (see available_doors.json)
##
## result: 
##    JSON string containing a success or failure
@app.route("/api/v1/door/unlock/<door_name>", methods=["POST"])
def unlock(door_name):
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.unlock_door(user, pwd, door_name))



## lists doors that the user can unlock along with their IDs
## params: 
##    user- username (chs mina sidor) 
##    password - password (chs mina sidor)
##
## result: 
##    JSON string containing available doors
@app.route("/api/v1/door/available", methods=["GET"])
#@cache.cached(timeout=300)
def available_doors():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.get_available_doors(user, pwd))



## lists booked machines along with dates from mina sidor
## params:
##    user - username (chs mina sidor) 
##    password - password (chs mina sidor)
##
## result:
##    JSON string containing booked laundry rooms
@app.route("/api/v1/laundry/schedule", methods=["GET"])
#@cache.cached(timeout=300, key_prefix=__make_cache_key)
def laundry_schedule():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.get_laundry_bookings(user, pwd))



## fetches x closest machines available to book
## params:
##    user - username (chs mina sidor) 
##    password - password (chs mina sidor)
##    num - number of available machines to display (OPTIONAL, default is 10)
##
## result:
##    JSON string containing available machines and their associated data.
@app.route("/api/v1/laundry/available/<num>", methods=["GET"])
#@cache.cached(timeout=300)
def available_machines(num):
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.get_available_machines(user, pwd, num))



## books given laundry machine 
## params:
##    user  - username (chs mina sidor) 
##    pwd  - password (chs mina sidor)
##    bookingGroupNo  - Booking Group Number
##    passNo  - Pass No
##    passDate  - passDate (ISO YYYY-MM-DD)
##
## result:
##    JSON string containing a success or failure 
@app.route("/api/v1/laundry/book", methods=["POST"])
def laundry_book():
    user = request.form["user"]
    pwd = request.form["password"]
    booking_group_no = request.args.get("bookingGroupNo")
    pass_no = request.args.get("passNo")
    pass_date = request.args.get("passDate")

  #  cache.delete(__make_cache_key())
    return jsonify(aptus.book_machine(user, pwd, str(booking_group_no), str(pass_no), str(pass_date)))



## cancels a booking
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
##    machine_id - id of machine
##
## result:
##    JSON string containing a success or failure
@app.route("/api/v1/laundry/unbook/<machine_id>", methods=["POST"])
def laundry_cancel(machine_id):
    user = request.form["user"]
    pwd = request.form["password"]

 #   cache.delete(__make_cache_key())
    return jsonify(aptus.unbook_machine(user, pwd, str(machine_id)))



## Returns a sum of paid, unpaid and pending rent invoices (avisummering)
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
## 
##
## result:
##    JSON string containing amount of paid, unpaid and pending
@app.route("/api/v1/invoice/sum", methods=["GET"])
#@cache.cached(timeout=300, key_prefix=__make_cache_key)
def invoice_sum():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.get_invoice_sum(user, pwd))



## Retrieves details about invoices (hyresavi)
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
## 
##
## result:
##    JSON string containing invoices
@app.route("/api/v1/invoice/list", methods=["GET"])
#@cache.cached(timeout=300, key_prefix=__make_cache_key)
def invoice_list():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.get_invoice_list(user, pwd))



## Retrieves contact info for user
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
## 
##
## result:
##    JSON string containing user info
@app.route("/api/v1/contact/info", methods=["GET"])
#@cache.cached(timeout=300, key_prefix=__make_cache_key)
def contact_info():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.get_contact_info(user, pwd))



## Retrieves the latest news from Chalmers Studentbostäder
## params:
##    news_category - What type of news to fetch
##                      e.g (nyheter, omradesnyheter)   
##
##
## result:
##    JSON string containing latest news from leaser
@app.route("/api/v1/news/<news_category>", methods=["GET"])
#@cache.cached(timeout=300)
def news(news_category):
    return jsonify(aptus.get_news(news_category))



## Destroys cache of user. Used for debugging purposes
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
##
##
## result:
##    Acknowledgement of destroyed cache
@app.route("/api/v1/cache/destroy", methods=["GET"])
def destroy_cache():
    user = request.form["user"]
    pwd = request.form["password"] 

 #   cache.delete(__make_cache_key())
    return jsonify(status="success", data="Cache destroyed for user: " + user)