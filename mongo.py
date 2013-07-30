from bson.objectid import ObjectId
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
    return entries.find_one({"lat": location.lat, "lng": location.lng})

def view_location(location_id = None):
    entries = db.entries

    if location_id:
        locations = entries.find({ "_id" : ObjectId(location_id) })
    else:
        locations = list(entries.find())

    return [Location(name = location['name'], 
        lat = location['lat'], 
        lng = location['lng'], 
        address = location['address']) for location in locations]

def update_location(location, location_id):
    entries = db.entries
    old_entry = list(entries.find({"_id": ObjectId(location_id)}))
    entries.update(old_entry[0], {"$set": location.jsonify()})

    return entries.find_one({ "_id" : ObjectId(location_id)})

def delete_location(location_id):
    entries = db.entries

    entries.remove({"_id": ObjectId(location_id)})
    found = entries.find({"_id": ObjectId(location_id)})
    if found:
        return False
    return True


