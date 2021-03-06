from flask import Flask, request, jsonify
from __init__ import app, db, ma
from Models import Location, User

db.create_all()

@app.route('/user', methods=['POST'])


@app.route('/update-location', methods=['POST'])
def add_location():
    user_id = request.json['user_id']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    new_location = Location.Location(user_id=user_id, latitude=latitude, longitude=longitude)
    db.session.add(new_location)
    db.session.commit()
    location_schema = Location.LocationSchema()
    data = location_schema.dump(new_location)
    data['message'] = "Location added"
    return data, 201


@app.route('/location/<user_id>', methods=['GET'])
def get_locations(user_id):
    locations = Location.Location.query.filter_by(user_id = user_id).all()
    location_schema = Location.LocationSchema(many=True)
    result = location_schema.dump(locations)
    return jsonify(result)


#Run Server
if __name__ == '__main__':
    app.run()
