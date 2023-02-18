import requests
import urllib.parse
from typing import Union
from datetime import datetime, time, date, timedelta
import json
import os


tr_table = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")

if os.path.exists("cities.json"):
    with open("cities.json") as f:
        turkey_cities = json.load(f)
else:
    turkey = ["İstanbul","Ankara","İzmir","Bursa","Antalya","Kahramanmaraş","Gaziantep","Kütahya","Çanakkale",
              "Mersin","Manisa","Adana","Niğde","Diyarbakır","Şanlıurfa","Mardin","Batman","Şırnak","Kocaeli",
              "Sakarya","Denizli","Aydın","Afyonkarahisar","Isparta","Burdur","Muğla","Konya","Trabzon","Rize",
              "Elazığ","Nevşehir","Samsun","Tokat","Düzce","Aksaray","Kayseri","Çorum","Gümüşhane","Artvin","Ordu",
              "Kastamonu","Giresun","Amasya","Eskişehir","Erzurum","Hatay","Hakkari","Kars","Erzincan","Tekirdağ",
              "Ağrı","Edirne","Malatya","Kırıkkale","Adıyaman","Uşak","Yozgat","Zonguldak","Van","Balıkesir","Bilecik",
              "Bingöl","Karabük","Karaman","Bolu","Osmaniye","Çankırı","Bartın","Bayburt","Sivas","Yalova","Bitlis",
              "Siirt","Sinop","Kırşehir","Ardahan","Kırklareli","Muş","Kilis","Tunceli","Iğdır"]

    replacements = {"ı": "i", "Ş": "S","ş": "s", "ç": "c","Ç": "C", "ü": "u","Ü": "U","Ğ": "G", "ğ": "g", "İ": "i"}
    turkey_cities = {"".join([replacements.get(c, c) for c in i]).lower(): i for i in turkey}
    
    with open("cities.json", "w", encoding='utf-8') as f:
        json.dump(turkey_cities, f)

host = "https://namaz-vakti.vercel.app"
endpoint = "/api/timesFromPlace?country=Turkey&region={0}&city={0}&date={1}&days=1&timezoneOffset=180"


def fetch_pray_info(city: str):
    vakts = {"imsak": None,
             "gunes": None,
             "ogle": None,
             "ikindi": None,
             "aksam": None,
             "yatsi": None}
       
    date_string = date.today().strftime("%Y-%m-%d")
    url = host + endpoint.format(turkey_cities.get(city), date_string)
    print(url)
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(e)
        raise "Cannot fetch data from api server ..."
    
    for i, vakt in enumerate(vakts.keys()):
        vakts[vakt] = data['times'][date_string][i]
    print(vakts)    
    return vakts

def url_encode(data: dict):
    return {k: urllib.parse.quote_plus(v) for k, v in data.items()}

def correct_tr(string):
    return string.translate(tr_table)
    
def calc_remaining_time(city):
    current_time = datetime.now()  # returns datetime object
    try:
        vakts = fetch_pray_info(city)
    except Exception as e:
        raise "Error occured while executing fetch_pray_info funtion"
    vakts_converted = dict()
    for k, v in vakts.items():
        vakts_converted[k] = convert_to_datetime(v)
    
    # current_pray_time_tag 

def convert_to_datetime(time_str, day_offset=None):
    if day_offset is None:
        dt = date.today()
    else:
        dt = date.today() + timedelta(days=day_offset)
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    datetime_obj = datetime.combine(dt, time_obj)
    
    return datetime_obj


namazlar = {"imsak" :  "06:26",
            "gunes" :  "07:52",
            "ogle" :   "13:24",
            "ikindi" : "16:17",
            "aksam" :  "18:46",
            "yatsi" :  "20:06"}


def get_pray_info(vakts: dict, as_str=False, time_offset=None) -> dict:
    if time_offset is None:
        time_offset = datetime.now()

    response = {"Date": str(date.today()) if as_str else date.today(),
                "CurrentTime": time_offset.strftime('%H:%M') if as_str else time_offset,
                "CurrentPrayer": None ,
                "RemainingTimeToNextPray": None,
                "NextPrayerTime": None,
            }
    if convert_to_datetime(vakts['imsak']) <= time_offset < convert_to_datetime(vakts['gunes']):
        response["CurrentPrayer"] = "sabah namaz vakti"
        response["NextPrayerTime"] = "ogle"
    elif convert_to_datetime(vakts['gunes']) <= time_offset < convert_to_datetime(vakts['ogle']):
        response["CurrentPrayer"] = "kusluk vakti"
        response["NextPrayerTime"] = "ogle"
    elif convert_to_datetime(vakts['ogle']) <= time_offset < convert_to_datetime(vakts['ikindi']):
        response["CurrentPrayer"] = "ogle namaz vakti"
        response["NextPrayerTime"] = "ikindi"
    elif convert_to_datetime(vakts['ikindi']) <= time_offset < convert_to_datetime(vakts['aksam']):
        response["CurrentPrayer"] = "ikindi namaz vakti"
        response["NextPrayerTime"] = "aksam"
    elif convert_to_datetime(vakts['aksam']) <= time_offset < convert_to_datetime(vakts['yatsi']):
        response["CurrentPrayer"] = "aksam namaz vakti"
        response["NextPrayerTime"] = "yatsi"
    elif convert_to_datetime(vakts['yatsi']) <= time_offset < convert_to_datetime(vakts['imsak'], day_offset=1):
        response["CurrentPrayer"] = "yatsi namaz vakti"
        response["NextPrayerTime"] = "imsak"
    elif convert_to_datetime(vakts['yatsi'], day_offset=-1) <= time_offset < convert_to_datetime(vakts['imsak']):
        response["CurrentPrayer"] = "yatsi namaz vakti"
        response["NextPrayerTime"] = "imsak"
    else:
        print("Error")

    time_left = convert_to_datetime(vakts[response["NextPrayerTime"]]) - time_offset
    str_time_left = str(time_left)
    response["RemainingTimeToNextPray"] = str_time_left if as_str else time_left

    
    return response

def freetime_info(city: str, time_after: int, duration: tuple[int, int]):

    meeting_duration = timedelta(hours=duration[0], minutes=duration[1])
    meeting_time =datetime.now() + timedelta(hours=time_after)
    
    response = get_pray_info(fetch_pray_info(city=city), as_str=False, time_offset=meeting_time)
    recommend = []
    if response["CurrentPrayer"] == "ikindi":
        recommend.append("you will be ikindi pray time at your meeting start time")
        recommend.append(f"Time Left to aksam pray time after the end of the meeting --> {response['RemainingTimeToNextPray']}")
        if response["RemainingTimeToNextPray"] < timedelta(minutes=45):
            recommend.append("if you perform the meeting at that time, you will be in the kerahat time after the end of the meeting!")
            recom_meet_dur = meeting_duration - response["RemainingTimeToNextPray"]
            recommend.append(f"Recommended meeting duration --> {recom_meet_dur}")
    elif response["RemainingTimeToNextPray"] < timedelta(minutes=30):
        recommend.append("Take care of remaining time to next pray ! less than 30 minutes!")

    else:
        recommend.append(f"Good Time for meeting {str(meeting_time)}")


    return {"MeetingTime": meeting_time.strftime('%H:%M'),
            "TimeOffset": response["CurrentTime"].strftime('%H:%M'),
            "PrayerTimeTagOnMeetingTime": response["CurrentPrayer"],
            "RemainingTimeToNextPray": str(response["RemainingTimeToNextPray"]),
            "NextPrayerTime": response["NextPrayerTime"],
            "Recommendations": recommend}


#print(convert_to_datetime("06:26"))      
#print(convert_to_datetime("06:26", next_day=True))
#print(datetime.now() + timedelta(hours=6, minutes=26))
#print(convert_to_datetime(namazlar['yatsi']))


#print(get_pray_info(namazlar))

current_time = datetime.now()
print(current_time)
if convert_to_datetime(namazlar['imsak']) <= current_time < convert_to_datetime(namazlar['gunes']):
    print({"CurrentPrayer":"sabah namaz vakti",
           "NextPrayerTime":"ogle"})
elif convert_to_datetime(namazlar['gunes']) <= current_time < convert_to_datetime(namazlar['ogle']):
    print({"CurrentPrayer":"kusluk vakti",
           "NextPrayerTime":"ogle"})
elif convert_to_datetime(namazlar['ogle']) <= current_time < convert_to_datetime(namazlar['ikindi']):
    print({"CurrentPrayer":"ogle namaz vakti",
           "NextPrayerTime":"ikindi"})
elif convert_to_datetime(namazlar['ikindi']) <= current_time < convert_to_datetime(namazlar['aksam']):
    print({"CurrentPrayer":"ikindi namaz vakti",
           "NextPrayerTime":"aksam"})
elif convert_to_datetime(namazlar['aksam']) <= current_time < convert_to_datetime(namazlar['yatsi']):
    print({"CurrentPrayer":"aksam namaz vakti",
           "NextPrayerTime":"yatsi"})
elif convert_to_datetime(namazlar['yatsi']) <= current_time < convert_to_datetime(namazlar['imsak'], day_offset=1):
    print({"CurrentPrayer":"yatsi namaz vakti",
           "NextPrayerTime":"imsak"})
elif convert_to_datetime(namazlar['yatsi'], day_offset=-1) <= current_time < convert_to_datetime(namazlar['imsak']):
    print({"CurrentPrayer":"yatsi namaz vakti",
           "NextPrayerTime":"imsak"})
else:
    print("errror")

#print(convert_to_datetime(namazlar['imsak'], next_day=True) > current_time)
#print(convert_to_datetime(namazlar['yatsi']) < current_time)

#print(convert_to_datetime("02:00", day_offset=-1))







        
