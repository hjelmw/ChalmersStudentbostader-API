from flask import Flask, jsonify, request
from aptus import unlockDoor, getLaundryBookings

app = Flask(__name__)



## opens one of the doors controlled by Aptusport
## params: 
##    username (chs mina sidor), 
##    password (chs mina sidor), 
##    id of door to unlock (see available_doors.json)
##
## result: 
##    JSON string containing a success or failure
@app.route('/api/v1/door/unlock', methods=['POST'])
def unlock():
    usr = request.form['usr']
    pwd = request.form['pwd']
    door_name = request.form['door_name']
    return jsonify(
        status = 'success',
        data = unlockDoor(usr, pwd, door_name), 
        mimetype = 'application/json'
    )


## lists booked laundry rooms along with dates from mina sidor
## params:
##    username (chs mina sidor)
##    password (chs mina sidor)
##
## result:
##    JSON string containing booked laundry rooms
@app.route('/api/v1/laundry/schedule', methods=['GET'])
def laundrySchedule():
    usr = request.form['usr']
    pwd = request.form['pwd']
    return jsonify(
        status = 'success',
        data = getLaundryBookings(usr, pwd),
        mimetype = 'application/json'
    )

## books given laundry machine 
## params:
##    username (chs mina sidor)
##    password (chs mina sidor)
##    id of machine (see available_machines.json)    
##
## result:
##    JSON string containing a success or failure
@app.route('/api/v1/laundry/book')
def laundryBook():
    return 0

## cancels a booking
## params:
##    username (chs mina sidor)
##    password (chs mina sidor)
##    id of machine or timestamp
##
## result:
##    JSON string containing a success or failure
@app.route('/api/v1/laundry/cancel')
def laundryCancel():
    return 0


@app.route('/test')
def test():
    return 'helloworld'