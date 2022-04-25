# ChalmersStudentbostader-API
## Update!
It was cool while it lasted but since I have not kept this API up-to-date for a few years it no longer functions. However, if you want to write your own REST-API for Chalmers Student Housing this can probably be used as some sort of reference at the very least!

## Introduction
A simple REST-API for wrapping around the services for tenants of Chalmers Studentbostäder (Student Housing) [mina sidor](https://www.chalmersstudentbostader.se/min-bostad/). 

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

# Testing
Tests are written in [pytest](https://docs.pytest.org/en/latest/). See [/test](/test) for details.


# Usage
Check out available requests on Postman. You can view the [documentation](https://documenter.getpostman.com/view/6066375/S1EUtF9a) or click the button below to import the colletion to your own Postman app.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c37165aed8d58936867b)

### Example Request & Response
```
GET /api/v1/laundry/available/2
Body: 
user=<user>
password=<password>
```
```json
200 OK
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

### News 📰
 * Get the latest and greatest from Stiftelsen Chalmers Studenbostäder (Currently Swedish 🇸🇪 only)


# In progress (maybe)
 * Change tenant info
 * Queue days
