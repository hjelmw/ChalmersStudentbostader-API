from flask import Flask, jsonify, request, redirect, url_for
from flask_caching import Cache
import aptus

app = Flask(__name__)
cache = Cache(app, config = {"CACHE_TYPE" : "simple"})

## for Flask-Cache
## generates cache key based on user and password in form-data of request
def __make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.form["user"] + request.form["password"])))
    return (path + args).encode('utf-8')



## opens one of the doors controlled by Aptusport
## params: 
##    usr- username (chs mina sidor) 
##    pwd - password (chs mina sidor)
##    id of door to unlock (see available_doors.json)
##
## result: 
##    JSON string containing a success or failure
@app.route("/api/v1/door/unlock/<door_name>", methods=["POST"])
def unlock():
    user = request.form["user"]
    pwd = request.form["password"]
    return jsonify(aptus.unlockDoor(user, pwd, door_name))



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
@app.route("/api/v1/laundry/available/<num>", defaults={"num" : "1"}, methods=["GET"])
@cache.memoize(timeout=60)
def AvailableMachines(num):
    user = request.form["user"]
    pwd = request.form["password"]
    print(num)
    return jsonify(aptus.getAvailableMachines(user, pwd, num))



## books given laundry machine 
## params:
##    usr  - username (chs mina sidor) 
##    pwd  - password (chs mina sidor)
##    grp  -     
##    date - starting date for when to book machine (ISO YYYY-MM-DD)
##
## result:
##    JSON string containing a success or failure 
@app.route("/api/v1/laundry/book/", methods=["POST"])
def laundryBook():
    user = request.form["user"]
    pwd = request.form["password"]
    bookingGrpNo = request.form["bookingGroupNo"]
    passNo = request.form["passNo"]
    passDate = request.form["passDate"]
    return jsonify(
        status = "success",
        data = aptus.bookMachine(user, pwd, bookingGrpNo, passNo, passDate),
        mimetype = "application/json"
    )


## TODO implement
## cancels a booking
## params:
##    usr - username (chs mina sidor)
##    pwd - password (chs mina sidor)
##    id of machine or timestamp
##
## result:
##    JSON string containing a success or failure
@app.route("/api/v1/laundry/cancel", methods=["POST"])
def laundryCancel():

    #clear cache
    cache.delete_memoized("test")
    return 0


