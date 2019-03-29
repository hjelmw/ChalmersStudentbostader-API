# chs-studentbostader-api
A simple REST-API for wrapping around the services for tenants of Chalmers Studentbostäder [mina sidor](https://www.chalmersstudentbostader.se/min-bostad/). 

The API is built on the microframework [Flask](http://flask.pocoo.org/) and uses a mix of web scraping and API calls to a "hidden" REST API maintaned by Aptusport.

# Installation
Install Flask framework and dependencies
```
pip install -U Flask
pip install requests lxml
```
Start app with
```
FLASK_APP=app.py
flask run
```
Server will start on `localhost:5000` See Usage for example requests


# Usage
TODO Add Postman Collection

# Finished features
 * Open front doors of buildings operated by Aptusport Emilsborg 🔑🚪
 * View your currently booked laundry schedule
 * View X amount of closest available laundry times
 * Book a laundry room

# In progress
 * Cancel a scheduled laundry booking
 * View rent invoices
 * View and change tenant info (phone number, email etc).
