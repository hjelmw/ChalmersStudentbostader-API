# chs-studentbostader-api
A simple REST-API for wrapping around the services for tenants of Chalmers Studentbostäder [mina sidor](https://www.chalmersstudentbostader.se/min-bostad/). 

The API is built on the microframework [Flask](http://flask.pocoo.org/) and uses a mix of web scraping and API calls to a "hidden" REST API maintaned by Aptusport.

# Installation
Install Flask framework and dependencies
```
pip install -U Flask
pip install -U Flask-Caching
pip install requests lxml
```
Start app with
```
FLASK_APP=app.py
flask run
```
Server will start on `localhost:5000` See Usage for example requests


# Usage
Check out available requests on Postman. You can view the [documentation](https://documenter.getpostman.com/view/6066375/S1EUtF9a) or click the button below to import the colletion to your own Postman app.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c37165aed8d58936867b)

### Example Request & Response
```
GET /api/v1/laundry/available/2
Content-Type: application/json
Body: 
user=<user>
password=<password>
```
```
200 OK
Content-Type: application/json
Server: Werkzeug/0.15.2 Python/3.7.2
Body:
{
	"status": "success",
	"data": {
		"0": {
			"bookingGroupId": "47",
			"date": "SÖN 21 APR",
			"laundry_room": "Tvättstuga 3",
			"passDate": "2019-04-21",
			"passNo": "7",
			"street": "EB 84 Tvättstuga 1-5",
			"time": "19:00-21:30"
		},
		"1": {
			"bookingGroupId": "49",
			"date": "SÖN 21 APR",
			"laundry_room": "Tvättstuga 5",
			"passDate": "2019-04-21",
			"passNo": "7",
			"street": "EB 84 Tvättstuga 1-5",
			"time": "19:00-21:30"
		}
	}
}
```

# Finished features
#### Doors 🔑🚪
  * Open front doors of buildings operated by Aptusport and available on [mina sidor](https://www.chalmersstudentbostader.se/min-bostad/)
  * View available doors to open
 
#### Laundry 🧺
 * Book a laundry room
 * Cancel a scheduled laundry machine booking
 * View your current laundry schedule
 * View X amount of closest available laundry times

#### Rent and invoices (hyresavi) 📝
 * View summary of paid, unpaid and pending invoices
 * View detailed info on rent invoices and their status
 
### Tenant 👱
 * View tenant info (name, phone, email etc)

# In progress (maybe)
 * Change tenant info
 * Queue days
