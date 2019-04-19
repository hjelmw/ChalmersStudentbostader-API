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
TODO Add Postman Collection

# Finished features
#### Doors 🔑🚪
  * Open front doors of buildings operated by Aptusport and available on [mina sidor](https://www.chalmersstudentbostader.se/min-bostad/)
  * View available doors to open
 
#### Laundry 🧺
 * Book a laundry room
 * Cancel a scheduled laundry machine booking
 * View your current laundry schedule
 * View X amount of closest available laundry times

#### Misc
 * View rent invoices and their status (pending/paid etc) (Hyresavi)

# In progress
 * View and change tenant info (phone number, email etc).
 * View available laundry times on specific date
