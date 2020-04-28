from flask import Flask, request, jsonify
from __init__ import app, db, ma
from Models import User, Location, Notification

db.create_all()

@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    address = request.json['address']
    mobile = request.json['mobile']

    new_user = User.User(name=name, email=email, address=address, mobile=mobile)

    db.session.add(new_user)
    db.session.commit()
    user_schema = User.UserSchema()
    return user_schema.jsonify(new_user)


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.User.query.get(id)
    user_schema = User.UserSchema()
    return user_schema.jsonify(user)


@app.route('/location', methods=['POST'])
def add_location():
    user_id = request.json['user_id']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    new_location = Location.Location(user_id=user_id, latitude=latitude, longitude=longitude)
    db.session.add(new_location)
    db.session.commit()
    location_schema = Location.LocationSchema()
    return location_schema.jsonify(new_location)


@app.route('/location/<user_id>', methods=['GET'])
def get_locations(user_id):
    locations = Location.Location.query.filter_by(user_id = user_id).all()
    location_schema = Location.LocationSchema(many=True)
    result = location_schema.dump(locations)
    return jsonify(result)


#Run Server
if __name__ == '__main__':
    app.run()