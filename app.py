from flask import Flask, jsonify, request
import aptus

app = Flask(__name__)



## opens one of the doors controlled by Aptusport
## params: 
##    usr- username (chs mina sidor) 
##    pwd - password (chs mina sidor)
##    id of door to unlock (see available_doors.json)
##
## result: 
##    JSON string containing a success or failure
@app.route("/api/v1/door/unlock", methods=["POST"])
def unlock():
    user = request.form["user"]
    pwd = request.form["password"]
    door_name = request.form["door"]
    return jsonify(aptus.unlockDoor(user, pwd, door_name))



## lists booked machines along with dates from mina sidor
## params:
##    usr - username (chs mina sidor) 
##    pwd - password (chs mina sidor)
##
## result:
##    JSON string containing booked laundry rooms
@app.route("/api/v1/laundry/schedule", methods=["GET"])
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
@app.route("/api/v1/laundry/available", methods=["GET"])
def AvailableMachines():
    user = request.form["user"]
    pwd = request.form["password"]
    num = request.form["num"]
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
@app.route("/api/v1/laundry/book", methods=["POST"])
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
    return 0
