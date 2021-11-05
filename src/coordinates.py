import requests
import json

def getCoordinates(hotel):
  if hotel['address'] == None :
    hotel['coordinates'] = None
    return

  try:
    r = requests.get(f'https://nominatim.openstreetmap.org/search?q={"+".join(hotel["address"].split(" "))}&format=geojson').content
    coords = json.loads(r)['features'][0]['geometry']['coordinates']
    hotel['coordinates'] = {'latitude': coords[1], 'longitude': coords[0]}
  except (IndexError, json.JSONDecodeError):
    hotel['coordinates'] = None
