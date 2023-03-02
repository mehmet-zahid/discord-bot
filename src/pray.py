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
endpoint = "/api/timesFromPlace?country=Turkey&region={0}&city={0}&date={1}&days=3&timezoneOffset=180"

PRAYERS_EN = ["Fajr", "Tulu", "Zuhr", "Asr", "Maghrib", "Isha"]
BISMILLAH = '\u0628\u0650\u0633\u0652\u0645\u0650\u0020\u0627\u0644\u0644\u0651\u064e\u0647\u0650\u0020\u0627\u0644\u0631\u0651\u064e\u062d\u0652\u0645\u064e\u0627\u0646\u0650\u0020\u0627\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645\u0650'
def fetch_pray_info(city: str):
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    vakts = {"yesterday": {"date": yesterday,
                           "prays": {"imsak": None,
                                     "gunes": None,
                                     "ogle": None,
                                     "ikindi": None,
                                     "aksam": None,
                                     "yatsi": None
                                     }
                          },
             "today": {"date": today,
                       "prays": {"imsak": None,
                                 "gunes": None,
                                 "ogle": None,
                                 "ikindi": None,
                                 "aksam": None,
                                 "yatsi": None
                                }
                       },
             "tomorrow": {"date": tomorrow,
                          "prays": {"imsak": None,
                                    "gunes": None,
                                    "ogle": None,
                                    "ikindi": None,
                                    "aksam": None,
                                    "yatsi": None
                                    }
                          }
            }
    
    url = host + endpoint.format(turkey_cities.get(city), vakts['yesterday']['date'])
    print(url)
    try:
        response = requests.get(url).json()
        print(response)
    except Exception as e:
        print(e)
        raise "Cannot fetch data from api server ..."
    
    date_keys = {yesterday: 'yesterday', today: 'today', tomorrow: 'tomorrow'}

    # Fill in the prayer times for each day
    for day, times in response['times'].items():
        if day in date_keys:
            key = date_keys[day]
            vakts[key]['prays']['imsak'] = times[0]
            vakts[key]['prays']['gunes'] = times[1]
            vakts[key]['prays']['ogle'] = times[2]
            vakts[key]['prays']['ikindi'] = times[3]
            vakts[key]['prays']['aksam'] = times[4]
            vakts[key]['prays']['yatsi'] = times[5] 
    return vakts

def url_encode(data: dict):
    return {k: urllib.parse.quote_plus(v) for k, v in data.items()}

def correct_tr(string):
    return string.translate(tr_table)

def set_global_view(vakts: dict):
    return dict(map(lambda x: (x[0].capitalize() + '-' + '('+ x[1] + ')', vakts[x[0]]), zip(vakts.keys(), PRAYERS_EN)))
   

    
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

def convert_to_datetime(time_str, day_offset=None, date_string=None):
    if date_string:
        dt = datetime.strptime(date_string, '%Y-%m-%d')
    elif day_offset is None:
        dt = date.today()
    else:
        dt = date.today() + timedelta(days=day_offset)
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    datetime_obj = datetime.combine(dt, time_obj)
    
    return datetime_obj



def get_pray_info(vakts: dict, as_str=False, time_offset=None) -> dict:
    if time_offset is None:
        time_offset = datetime.now()
    buff = vakts.copy()
    try:
        for k, v in vakts.items():
            print(v)
            for x, y in v.items():
                if x == 'prays':
                    for a, b in y.items():
                        buff[k][x][a] = convert_to_datetime(b, date_string=vakts[k]['date'])
    except Exception as e:
        print(e)
    print(buff)

    response = {"Date": str(date.today()) if as_str else date.today(),
                "CurrentTime": time_offset.strftime('%H:%M') if as_str else time_offset,
                "CurrentPrayer": None ,
                "TimeLeft": None,
                "NextPrayerTime": None,
            }
    if buff['today']['prays']['imsak'] <= time_offset < buff['today']['prays']['gunes']:
        response["CurrentPrayer"] = "Sabah Vakti"
        response["NextPrayerTime"] = "Ogle"
        response["TimeLeft"] = buff['today']['prays']['ogle'] - time_offset
    
    elif buff['today']['prays']['gunes'] < time_offset <= buff['today']['prays']['gunes'] + timedelta(minutes=50):
        response["CurrentPrayer"] = "Kerahat Vakti"
        response["NextPrayerTime"] = "Ogle"
        response["TimeLeft"] = buff['today']['prays']['ogle'] - time_offset

    elif buff['today']['prays']['gunes'] + timedelta(minutes=50) <= time_offset < buff['today']['prays']['ogle'] - timedelta(minutes=50):
        response["CurrentPrayer"] = "İşrak Vakti"
        response["NextPrayerTime"] = "Ogle"
        response["TimeLeft"] = buff['today']['prays']['ogle'] - time_offset
    
    elif buff['today']['prays']['ogle'] - timedelta(minutes=50) <= time_offset < buff['today']['prays']['ogle']:
        response["CurrentPrayer"] = "Dahve-i Kubra"
        response["NextPrayerTime"] = "Ogle"
        response["TimeLeft"] = buff['today']['prays']['ogle'] - time_offset

    elif buff['today']['prays']['ogle'] <= time_offset < buff['today']['prays']['ikindi']:
        response["CurrentPrayer"] = "Ogle Vakti"
        response["NextPrayerTime"] = "İkindi"
        response["TimeLeft"] = buff['today']['prays']['ikindi'] - time_offset

    elif buff['today']['prays']['ikindi'] <= time_offset < buff['today']['prays']['aksam']:
        response["CurrentPrayer"] = "İkindi Vakti"
        response["NextPrayerTime"] = "Aksam"
        response["TimeLeft"] = buff['today']['prays']['aksam'] - time_offset

    elif buff['today']['prays']['aksam'] <= time_offset < buff['today']['prays']['yatsi']:
        response["CurrentPrayer"] = "Aksam Vakti"
        response["NextPrayerTime"] = "Yatsi"
        response["TimeLeft"] = buff['today']['prays']['yatsi'] - time_offset

    elif buff['today']['prays']['yatsi'] <= time_offset < buff['tomorrow']['prays']['imsak']:
        response["CurrentPrayer"] = "Yatsi Vakti"
        response["NextPrayerTime"] = "İmsak"
        response["TimeLeft"] = buff['tomorrow']['prays']['imsak'] - time_offset

    elif buff['yesterday']['prays']['yatsi'] <= time_offset < buff['today']['prays']['imsak']:
        response["CurrentPrayer"] = "Yatsi Vakti"
        response["NextPrayerTime"] = "İmsak"
        response["TimeLeft"] = buff['today']['prays']['imsak'] - time_offset
    else:
        print("Error")
    
    
    str_time_left = str(response["TimeLeft"])
    response["TimeLeft"] = str_time_left if as_str else response["TimeLeft"]

    
    return response

def freetime_info(city: str, time_after: int, duration: tuple[int, int]):

    meeting_duration = timedelta(hours=duration[0], minutes=duration[1])
    meeting_time =datetime.now() + timedelta(hours=time_after)
    
    response = get_pray_info(fetch_pray_info(city=city), as_str=False, time_offset=meeting_time)
    recommend = []
    if response["CurrentPrayer"] == "ikindi":
        recommend.append("you will be ikindi pray time at your meeting start time")
        recommend.append(f"Time Left to aksam pray time after the end of the meeting --> {response['TimeLeft']}")
        if response["TimeLeft"] < timedelta(minutes=45):
            recommend.append("if you perform the meeting at that time, you will be in the kerahat time after the end of the meeting!")
            recom_meet_dur = meeting_duration - response["TimeLeft"]
            recommend.append(f"Recommended meeting duration --> {recom_meet_dur}")
    elif response["TimeLeft"] < timedelta(minutes=30):
        recommend.append("Take care of remaining time to next pray ! less than 30 minutes!")

    else:
        recommend.append(f"Good Time for meeting {str(meeting_time)}")


    return {"MeetingTime": meeting_time.strftime('%H:%M'),
            "MeetingDuration": str(meeting_duration),
            "TimeOffset": response["CurrentTime"].strftime('%H:%M'),
            "PrayerTimeTagOnMeetingTime": response["CurrentPrayer"],
            "TimeLeft": str(response["TimeLeft"]),
            "NextPrayerTime": response["NextPrayerTime"],
            "Recommendations": recommend}


#print(convert_to_datetime("06:26"))      
#print(convert_to_datetime("06:26", next_day=True))
#print(datetime.now() + timedelta(hours=6, minutes=26))
#print(convert_to_datetime(namazlar['yatsi']))
#print(get_pray_info(namazlar))
#print(convert_to_datetime(namazlar['imsak'], next_day=True) > current_time)
#print(convert_to_datetime(namazlar['yatsi']) < current_time)
#print(convert_to_datetime("02:00", day_offset=-1))

#print(fetch_pray_info("istanbul"))







        
