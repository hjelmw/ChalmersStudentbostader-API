import lxml.html
import requests
import json


session = requests.Session()

with open('doors.json') as file:
    available_doors = json.load(file)

def getAptusUrl(usr, pwd, sel):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
    session.post('https://www.chalmersstudentbostader.se/wp-login.php',
        data = {'log' : usr, 'pwd' : pwd},
        headers = {'User-Agent' : user_agent})
    r = session.get('https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=aptuslogin@APTUSPORT&widgets[]=aptuslogin')

    s = json.loads(r.text[2:-2])

    # aptusport or laundrybooking
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
    print('got url')
    print(laundry_url)
    res = session.get(laundry_url)
    print('got laundry site, checking')
    booking_cards = lxml.html.fromstring(res.content).xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]')
    
    # remove stupid whitespace and newline characters
    laundry_schedule = []
    for card in booking_cards:
        temp = {}
        temp['timestamp'] = card.xpath('.//button/@aria-label')[13:] 
        
        temp['duration'] = card.xpath('.//div[1]/text()')
        temp['day'] = card.xpath('.//div[2]/text()')
        temp['machines'] = card.xpath('.//div[4]/text()')
        temp['machines']['id'] = card.xpath(''  )
        temp['street'] = card.xpath('.//div[5]/text()')
        laundry_schedule.append(temp)
    return laundry_schedule

    #booking_timestamps = res.xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]/button/@aria-label')
    #booking_durations = res.xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]/div[1]')
    #booking_days = res.xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]/div[2]')
    #booking_machines =  res.xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]/div[4]')
    #booking_streets = res.xpath('/html/body/div/section/div[1]/div[1]/div[position()>1]/div[5]') 
    #bookings_json = { 'bookings' : []}
    #for i in range(len(booking_timestamps)):
    #    bookings_json['bookings'].append({
    #        'timestamp' : booking_timestamps[i][13:],
    #        'day' : booking_days[i],
    #        'duration' : booking_durations[i],
    #        'building' : booking_streets[i],
    #        'machine' : booking_machines[i]
    #    })
    #return bookings_json