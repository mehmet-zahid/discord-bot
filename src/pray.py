import requests
import urllib.parse
from typing import Union
from datetime import datetime, time, date, timedelta
import json
import os
import pytz

tz = pytz.timezone("Turkey")

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


def fetch_pray_info(city, pray_time_tag=None):
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

def convert_to_datetime(time_str):
    # time_str = '05:31'
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    datetime_obj = datetime.combine(datetime.today(), time_obj)

    return datetime_obj


namazlar = {"imsak" :  "06:26",
            "gunes" :  "07:52",
            "ogle" :   "13:24",
            "ikindi" : "16:17",
            "aksam" :  "18:46",
            "yatsi" :  "20:06"}


def get_pray_info(vakts: dict) -> dict:
    remainings = [] 
    current_time = datetime.now()
    tag_map = {0: "imsak",
               1: "gunes",
               2: "ogle",
               3: "ikindi",
               4: "aksam",
               5: "yatsi"}
    for k, v in vakts.items():
        rm_timedelta = current_time - convert_to_datetime(v)
        #if rm_timedelta < timedelta():
        #    continue
        remainings.append(rm_timedelta)
    rm_map = {}
    
    for i, tdelta in enumerate(remainings):
        if tdelta < timedelta():
            continue
        rm_map[i] = tdelta

    values = rm_map.values()
    min_value = min(values)
    
    for k, v in rm_map.items():
        if v == min_value:
            key = k

    return {"current_time": current_time.strftime('%H:%M'),
            "current_pray_time_tag": tag_map[key] ,
            "remaining_time_to_next_pray": str((convert_to_datetime(vakts[tag_map[key+1]]) - current_time)),
            "next_pray_time_tag": tag_map[key+1],
            }







        
