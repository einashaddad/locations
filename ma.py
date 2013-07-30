from flask import Flask, request, url_for, redirect, flash, abort, jsonify, make_response, Response
from models import Location
from pygeocoder import Geocoder
from bson.objectid import ObjectId
import json
import mongo
import os

app = Flask(__name__)

api_key = os.environ.get('GOOGLE_API_KEY')

@app.route('/api/locations', methods = ['POST'])
def create():
    '''
    Creates a location, given an address
    ''' 
    data = json.loads(request.data)
    if not data:
        abort(404)
    address = data['address']
    name = data['name']
    results = Geocoder.geocode(address)
    lat, lng = results[0].coordinates
    location = Location(lat=lat, lng=lng, name=name, address=address)
    result = mongo.create_location(location)
    return updated_jsonify(result)

@app.route('/api/locations/<location_id>', methods = ['GET'])
def view(location_id=None):
    '''
    Returns a location given the id
    '''
    if not location_id:
        abort(404)

    location_objects = mongo.view_location(location_id)
    location = [location_object.__dict__ for location_object in location_objects]
    return jsonify(results = location)
    

@app.route('/api/locations', methods = ['GET'])
def view_all():
    '''
    Returns a list of all locations
    '''
    list_of_location_objects = mongo.view_location()
    list_of_locations = [location_object.__dict__ for location_object in list_of_location_objects]
    return jsonify(results = list_of_locations)

@app.route('/api/locations/<location_id>', methods = ['PUT'])
def update(location_id):
    '''
    Edits/Updates the location
    '''
    if not location_id or request.data:
        abort(404)
    data = json.loads(request.data)
    new_name = data['name']
    new_address = data['address']
    results = Geocoder.geocode(new_address)
    new_lat, new_lng = results[0].coordinates
    
    location = Location(lat=new_lat, lng=new_lng, name=new_name, address=new_address)

    new_location = mongo.update_location(location_id=location_id, location=location)
    return updated_jsonify(new_location)

@app.route('/api/locations/<location_id>', methods = ['DELETE'])
def delete(location_id):
    if not location_id:
        abort(404)
    if not mongo.delete_location(location_id):
        return "OK"
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not Found'}), 404)

class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def updated_jsonify(data):
    return Response(json.dumps(data, cls=APIEncoder), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

