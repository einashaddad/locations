import pymongo
import os
from models import Location 

MONGOHQ_URL = os.environ.get('MONGOHQ_URL')

if MONGOHQ_URL:
  connection = pymongo.Connection(MONGOHQ_URL, safe=True)   # safe enables pymongo to wait to get all errors (getlasterror call)
  db = connection[urlparse(MONGOHQ_URL).path[1:]]   # this parses the app number from the url (app13974775)
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.test

def create_location(location):
    '''
    Saves the location
    '''
    entries = db.entries

    entries.insert(location.jsonify())

def view_location(name):
    entries = db.entries

    locations = entries.find({'name': name})
    
    return [Location(name = location['name'], 
            lat = location['lat'], 
            lng = location['lng'], 
            address = location['address']) for location in locations]

