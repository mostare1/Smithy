import requests
from flask import  jsonify

API_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Bucharest&key='
API_KEY = 'AIzaSyAg1UzzQSq382GMcSZAtjVVXjfeV96qTTw'

def results():
    url = API_URL 
    url += API_KEY
    search_json = requests.get(url).json()
    for restaurant in search_json['results']:
        print(restaurant['name'])