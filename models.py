
class Location(object):
    def __init__(self, lat, lng, address, name):
        #self.id = _id
        self.lat = lat
        self.lng = lng
        self.address = address
        self.name = name

    def jsonify(self):
        return {#'id': self.id,
                'lat': self.lat,
                'lng': self.lng,
                'address': self.address,
                'name': self.name, }

