import requests
import urllib.parse
from typing import Union
import datetime
import json
import os

tr_table = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")

if os.path.exists("cities.json"):
    with open("cities.json") as f:
        turkey_cities = json.load(f)
else:
    turkey = ["İstanbul","Ankara","İzmir","Bursa","Antalya","Kahramanmaraş","Gaziantep","Kütahya","Çanakkale","Mersin","Manisa","Adana","Niğde","Diyarbakır","Şanlıurfa","Mardin","Batman","Şırnak","Kocaeli","Sakarya","Denizli","Aydın","Afyonkarahisar","Isparta","Burdur","Muğla","Konya","Trabzon","Rize","Elazığ","Nevşehir","Samsun","Tokat","Düzce","Aksaray","Kayseri","Çorum","Gümüşhane","Artvin","Ordu","Kastamonu","Giresun","Amasya","Eskişehir","Erzurum","Hatay","Hakkari","Kars","Erzincan","Tekirdağ","Ağrı","Edirne","Malatya","Kırıkkale","Adıyaman","Uşak","Yozgat","Zonguldak","Van","Balıkesir","Bilecik","Bingöl","Karabük","Karaman","Bolu","Osmaniye","Çankırı","Bartın","Bayburt","Sivas","Yalova","Bitlis","Siirt","Sinop","Kırşehir","Ardahan","Kırklareli","Muş","Kilis","Tunceli","Iğdır"]
    replacements = {"ı": "i", "Ş": "S","ş": "s", "ç": "c","Ç": "C", "ü": "u","Ü": "U","Ğ": "G", "ğ": "g", "İ": "i"}
    turkey_cities = {"".join([replacements.get(c, c) for c in i]).lower(): i for i in turkey}
    
    with open("cities.json", "w", encoding='utf-8') as f:
        json.dump(turkey_cities, f)

print(turkey_cities.keys())
host = "https://namaz-vakti.vercel.app"
endpoint = "/api/timesFromPlace?country=Turkey&region={0}&city={0}&date={1}&days=1&timezoneOffset=180"


def fetch_pray_info(city, pray_time_tag=None):
    vakts = {"imsak": None,
             "sabah": None,
             "ogle": None,
             "ikindi": None,
             "aksam": None,
             "yatsi": None}
       
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    url = host + endpoint.format(turkey_cities.get(city), date_string)
    print(url)
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(e)
        return "Cannot fetch data from api server ..."
    
    for i, vakt in enumerate(vakts.keys()):
        vakts[vakt] = data['times'][date_string][i]
    print(vakts)    
    return vakts

def url_encode(data: dict):
    return {k: urllib.parse.quote_plus(v) for k, v in data.items()}

def correct_tr(string):
    return string.translate(tr_table)
    
def calc_availability():...
