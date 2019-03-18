from flask import Flask, jsonify, request
from aptus import unlockDoor, getLaundryBookings, getAvailableMachines, bookMachine

app = Flask(__name__)



## opens one of the doors controlled by Aptusport
## params: 
##    usr- username (chs mina sidor) 
##    pwd - password (chs mina sidor)
##    id of door to unlock (see available_doors.json)
##
## result: 
##    JSON string containing a success or failure
@app.route('/api/v1/door/unlock', methods=['POST'])
def unlock():
    usr = request.form['usr']
    pwd = request.form['pwd']
    door_name = request.form['door']
    return jsonify(
        status = 'success',
        data = unlockDoor(usr, pwd, door_name), 
        mimetype = 'application/json'
    )

## lists booked machines along with dates from mina sidor
## params:
##    usr - username (chs mina sidor) 
##    pwd - password (chs mina sidor)
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

## fetches x closest machines available to book
## params:
##    usr - username (chs mina sidor) 
##    pwd - password (chs mina sidor)
##    nom - number of available machines to display (OPTIONAL, default is 10)
##
## result:
##    JSON string containing available machines and their associated data.
@app.route('/api/v1/laundry/available', methods=['GET'])
def AvailableMachines():
    usr = request.form['usr']
    pwd = request.form['pwd']
    nom = request.form['x']
    return jsonify(
        status = 'success',
        data = getAvailableMachines(usr, pwd),
        mimetype = 'application/json'
    )

## books given laundry machine 
## params:
##    usr  - username (chs mina sidor) 
##    pwd  - password (chs mina sidor)
##    grp  - group id (see available_machines.json)    
##    pss  - booking pass number (?)
##    date - starting date for when to book machine (ISO xx-xx-xx)
##
## result:
##    JSON string containing a success or failure 
@app.route('/api/v1/laundry/book', methods=['POST'])
def laundryBook():
    usr = request.form['usr']
    pwd = request.form['pwd']
    grp = request.form['grp']
    pss = request.form['pss']
    date = request.form['date']
    return jsonify(
        status = 'success',
        data = bookMachine(usr, pwd, grp, pss, date),
        mimetype = 'application/json'
    )

## cancels a booking
## params:
##    usr - username (chs mina sidor)
##    pwd - password (chs mina sidor)
##    id of machine or timestamp
##
## result:
##    JSON string containing a success or failure
@app.route('/api/v1/laundry/cancel', methods=['POST'])
def laundryCancel():
    return 0


@app.route('/test')
def test():
    return 'helloworld'