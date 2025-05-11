
import requests
import os

GOOGLE_API_KEY = os.getenv('places_key')

def get_place_predictions(query, limit=5):
    autocomplete_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    params = {'input': query, 'key': GOOGLE_API_KEY}
    res = requests.get(autocomplete_url, params=params).json()
    return res.get('predictions', [])[:limit]

def get_coordinates_from_place_id(place_id):
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {'place_id': place_id, 'key': GOOGLE_API_KEY}
    res = requests.get(details_url, params=params).json()
    location = res.get('result', {}).get('geometry', {}).get('location', {})
    return location.get('lat'), location.get('lng')
