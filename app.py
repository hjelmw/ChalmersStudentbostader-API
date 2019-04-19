from flask import Flask, jsonify, request, redirect, url_for
from flask_caching import Cache
import aptus

app = Flask(__name__)
cache = Cache(app, config = {"CACHE_TYPE" : "simple"})

## for Flask-Cache
## generates cache key based on user and password in form-data of request
def __make_cache_key(*args, **kwargs):
    args = str(hash(request.form["user"] + request.form["password"] ))
    return (args).encode("utf-8")




############################# Error Routes #############################
@app.errorhandler(405)
def notAllowed(error):
    return jsonify(status = "error", data={"details": str(error),"message": "Are you using GET on a POST route?", "code": "405", "url":request.method + " " + request.path})

@app.errorhandler(404)
def pageNotFound(error):
    return jsonify(status = "error", data={"details": str(error), "message": "Check route path", "code": "404", "url": request.method + " " + request.path})

@app.errorhandler(500)
def internalServerError(error):
    return jsonify(status="error", data={"details": str(error),"message": "Internal server error. Something went wrong", "code": "500", "url": request.method + " " + request.path})

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
    return jsonify(aptus.unlockDoor(user, pwd, door_name))



## lists doors that the user can unlock along with their IDs
## params: 
##    user- username (chs mina sidor) 
##    password - password (chs mina sidor)
##
## result: 
##    JSON string containing available doors
@app.route("/api/v1/door/available", methods=["GET"])
@cache.cached(timeout=300, key_prefix=__make_cache_key)
def availableDoors():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.getAvailableDoors(user, pwd))



## lists booked machines along with dates from mina sidor
## params:
##    user - username (chs mina sidor) 
##    password - password (chs mina sidor)
##
## result:
##    JSON string containing booked laundry rooms
@app.route("/api/v1/laundry/schedule", methods=["GET"])
@cache.cached(timeout=60, key_prefix=__make_cache_key)
def laundrySchedule():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.getLaundryBookings(user, pwd))



## fetches x closest machines available to book
## params:
##    user - username (chs mina sidor) 
##    password - password (chs mina sidor)
##    num - number of available machines to display (OPTIONAL, default is 10)
##
## result:
##    JSON string containing available machines and their associated data.
@app.route("/api/v1/laundry/available/<num>", methods=["GET"])
@cache.cached(timeout=60)
def AvailableMachines(num):
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.getAvailableMachines(user, pwd, num))



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
def laundryBook():
    user = request.form["user"]
    pwd = request.form["password"]
    bookingGrpNo = request.args.get("bookingGroupNo")
    passNo = request.args.get("passNo")
    passDate = request.args.get("passDate")
    cache.delete(__make_cache_key())
    return jsonify(aptus.bookMachine(user, pwd, str(bookingGrpNo), str(passNo), str(passDate)))
        


## cancels a booking
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
##    machineId - id of machine
##
## result:
##    JSON string containing a success or failure
@app.route("/api/v1/laundry/unbook/<machine_id>", methods=["POST"])
def laundryCancel(machine_id):
    user = request.form["user"]
    pwd = request.form["password"]
    cache.delete_memoized(__make_cache_key())
    return jsonify(aptus.unbookMachine(user, pwd, str(machine_id)))


## Retrieves invoices (hyresavi)
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
## 
##
## result:
##    JSON string containing paid and unpaid invoices
@app.route("/api/v1/invoice/list", methods=["GET"])
@cache.cached(timeout=60, key_prefix=__make_cache_key)
def invoiceList():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.getInvoiceList(user, pwd))

    

## Destroys cache of user. Used for debugging purposes
## params:
##    user - username (chs mina sidor)
##    password - password (chs mina sidor)
##
##
## result:
##    Acknowledgement of destroyed cache
@app.route("/api/v1/cache/destroy")
def destroyCache():
    user = request.form["user"]
    pwd = request.form["password"] 
    cache.delete_memoized(__make_cache_key())
    return jsonify(status="success", data="Cache destroyed for user: " + __make_cache_key())