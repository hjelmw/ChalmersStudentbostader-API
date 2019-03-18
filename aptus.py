import lxml.html
import requests
import json

with open('doors.json') as file:
    available_doors = json.load(file)

session = requests.Session()
base_url = 'https://apt-www.chalmersstudentbostader.se/'

## helper function, returns the URL for aptusport or laundry services
## return format:
##     <baseURL>?module=<Lock|Booking>&customerName=<Customer>&timestamp=<Timestamp>&hash=<Hash>
def getAptusUrl(usr, pwd, sel):
    session.post('https://www.chalmersstudentbostader.se/wp-login.php', data = {'log' : usr, 'pwd' : pwd})
    r = session.get('https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=aptuslogin@APTUSPORT&widgets[]=aptuslogin')
    s = json.loads(r.text[2:-2])

    # var sel decides between aptusport or laundry services
    which_aptus = 'aptuslogin@APTUSPORT' if bool(sel) else 'aptuslogin'
    return json.loads(str(s['data'][which_aptus]['objekt'][0]).replace('\'',"\""))['aptusUrl']
    
def unlockDoor(usr, pwd, door_name):
    unlock_url = getAptusUrl(usr, pwd, True)
    session.get(unlock_url)
    res = session.get('https://apt-www.chalmersstudentbostader.se/AptusPortal/Lock/UnlockEntryDoor/' + available_doors[door_name])
    return {
        'door' : {
            'door_name' : door_name,
            'door_id' : available_doors[door_name]
        },
        'aptus_response' : json.loads(res.text)
    }

def getLaundryBookings(usr, pwd):
    laundry_url = getAptusUrl(usr, pwd, False)
    res = session.get(laundry_url)
    booking_cards = lxml.html.fromstring(res.content).xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]')
    
    ## TODO: remove whitespace and newline characters
    laundry_schedule = []
    for card in booking_cards:
        temp = {}
        temp['timestamp'] = card.xpath('.//button/@aria-label')[13:]     
        temp['duration'] = card.xpath('.//div[1]/text()')
        temp['day'] = card.xpath('.//div[2]/text()')
        temp['machines'] = card.xpath('.//div[4]/text()')
        temp['machines']['id'] = card.xpath('')
        temp['street'] = card.xpath('.//div[5]/text()')
        laundry_schedule.append(temp)
    return laundry_schedule

def getAvailableMachines(usr, pwd):
    laundry_url = getAptusUrl(usr, pwd, False)
    session.get(laundry_url)
    
    res = session.get(base_url + '/AptusPortal/CustomerBooking/FirstAvailable?categoryId=1&firstX=10')
    booking_cards = lxml.html.fromstring(res.content).xpath('/html/body/div/section/div/div')
    
    ## TODO: remove whitespace and newline characters
    available_machines = []
    for card in booking_cards:
        temp = {}
        temp['time'] = card.xpath('.//div[1]/text()')
        temp['date'] = card.xpath('.//div[2]/text()')
        temp['laundry room'] = card.xpath('.//div[4]/text()')
        temp['street'] = card.xpath('.//div[5]/text()')
        available_machines.append(temp)
    return available_machines

def bookMachine(usr, pwd, grp, timestamp):
    laundry_url = getAptusUrl(usr, pwd, False)
    session.get(laundry_url)
    res = session.get(base_url + '/AptusPortal/CustomerBooking/BookFirstAvailable?passNo='+pass_no+'&passDate='+timestamp+'&bookingGroupId='grp'')

    return 0