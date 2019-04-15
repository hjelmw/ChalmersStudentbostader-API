from flask import Flask, jsonify, request, redirect, url_for
from flask_caching import Cache
import aptus

app = Flask(__name__)
cache = Cache(app, config = {"CACHE_TYPE" : "simple"})

## for Flask-Cache
## generates cache key based on user and password in form-data of request
def __make_cache_key(*args, **kwargs):
    args = str(hash(request.form["user"] + request.form["password"]))
    return (args).encode("utf-8")

############################## FLASK ROUTES ##############################

## opens one of the doors controlled by Aptusport
## params: 
##    usr- username (chs mina sidor) 
##    pwd - password (chs mina sidor)
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
##    usr- username (chs mina sidor) 
##    pwd - password (chs mina sidor)
##
## result: 
##    JSON string containing available doors
@app.route("/api/v1/door/available", methods=["GET"])
@cache.cached(timeout=60)
def availableDoors():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.getAvailableDoors(user, pwd))


## lists booked machines along with dates from mina sidor
## params:
##    usr - username (chs mina sidor) 
##    pwd - password (chs mina sidor)
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
##    usr - username (chs mina sidor) 
##    pwd - password (chs mina sidor)
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
##    usr  - username (chs mina sidor) 
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
##    usr - username (chs mina sidor)
##    pwd - password (chs mina sidor)
##    machineId - id of machine or timestamp
##
## result:
##    JSON string containing a success or failure
@app.route("/api/v1/laundry/cancel/<machine_id>", methods=["POST"])
def laundryCancel(machine_id):
    user = request.form["user"]
    pwd = request.form["password"]
    cache.delete_memoized(__make_cache_key())
    return jsonify(aptus.unbookMachine(user, pwd, machine_id))


## Retrieves invoices (hyresavi)
## params:
##    usr - username (chs mina sidor)
##    pwd - password (chs mina sidor)
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
    