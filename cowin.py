import requests
from datetime import date
from datetime import timedelta
from datetime import datetime
import json
from fake_useragent import UserAgent
import schedule
import time
import webbrowser
from twilio.rest import Client

# Twillio Auth Token
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

def cowin_job():
    print("\nJob run at {}".format(datetime.now()))
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}

    for itr in range(4):
        try:
            today = datetime(2021,7,1) + timedelta(days=itr)
            currdate = today.strftime("%d-%m-%Y")
            for l in range(1):    
                pin = 482001+l
                response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin,currdate), headers=browser_header)
                json_data = json.loads(response.text)
                for i in json_data["sessions"]:
                    if i["vaccine"] == "COVAXIN" and i["min_age_limit"] == 18 and i["available_capacity_dose2"] > 0:
                        message = json.dumps(i, indent=4, sort_keys=True)
                        print(message)
                        message = client.messages .create(
                            body =  "ALERT! {} DOSES OF {} AVAILABLE AT {}. MESSAGE DISPATCHED AT {}.".format(i["available_capacity_dose1"],i["vaccine"],i["address"],datetime.now()),
                            from_ = "+15123796974", 
                            to =    "+918074170160")
                        message.sid
                        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', new=2)
                        exit()
        except Exception as e:
            print("Error: " + str(e))

schedule.every(42).seconds.do(cowin_job)

while True:
    schedule.run_pending()
    time.sleep(1)