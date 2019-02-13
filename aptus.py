import requests
import json
session = requests.Session()

with open('doors.json') as file:
    available_doors = json.load(file)

def getaptusurl(usr,pwd):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
    session.post('https://www.chalmersstudentbostader.se/wp-login.php',
        data = {'log' : usr, 'pwd' : pwd},
        headers = {'User-Agent' : user_agent})
    r = session.get('https://www.chalmersstudentbostader.se/widgets/?callback=?&widgets[]=aptuslogin')
    s = json.loads(r.text[2:-2])
    return json.loads(str(s['data']['aptuslogin']['objekt'][0]).replace('\'',"\""))['aptusUrl']

def unlockdoor(usr, pwd, door_name):
    aptusurl = getaptusurl(usr, pwd)
    session.get(aptusurl)
    res = session.get('https://apt-www.chalmersstudentbostader.se/AptusPortal/Lock/UnlockEntryDoor/' + available_doors[door_id])

    return {
        'door' : {
            'door_name' : door_name,
            'door_id' : available_doors[door_name]
        },
        'chs_response' : json.loads(res.text)
    }