from flask import Flask, render_template, request, url_for, redirect, session, flash, abort, jsonify
from models import Location
from pygeocoder import Geocoder
import json
import mongo
import os

app = Flask(__name__)

api_key = os.environ.get('GOOGLE_API_KEY')

@app.route('/create', methods = ['POST'])
def create():
    '''
    Creates a location, given an address
    ''' 
    data = json.loads(request.data)
    address = data['address']
    name = data['name']
    results = Geocoder.geocode(address)
    lat, lng = results[0].coordinates
    location = Location(lat=lat, lng=lng, name=name, address=address)
    mongo.create_location(location)
    return "OK"

@app.route('/view', methods = ['GET'])
def view():
    '''
    Returns the favorite location when looking up the name
    '''
    data = json.loads(request.data)
    name = data['name']
    
    list_of_location_objects = mongo.view_location(name)

    list_of_locations = [location_object.__dict__ for location_object in list_of_location_objects]

    return jsonify(results = list_of_locations)
    
    
    return "ok"
@app.route('/update')
def update():
    '''PUT'''
    pass

@app.route('/delete')
def delete():
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

