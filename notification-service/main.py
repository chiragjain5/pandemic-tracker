from flask import Flask, request, jsonify
from __init__ import app, db, ma
from Models import User, Location
from math import radians, cos, sin, asin, sqrt
from datetime import datetime, timedelta
from google.cloud import tasks
from os import environ, path
from dotenv import load_dotenv
import json

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


db.create_all()


def distance(latitude1, longitude1, latitude2, longitude2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    longitude1 = radians(longitude1)
    longitude2 = radians(longitude2)
    latitude1 = radians(latitude1)
    latitude2 = radians(latitude2)

    # Haversine formula
    dlon = longitude2 - longitude1
    dlat = latitude2 - latitude1

    a = sin(dlat / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result in meters
    return (c * r) * 1000


@app.route('/generate-notification', methods=['POST'])
def generate_notification():
    user_id = request.json['user_id']

    current_user_locations = Location.Location.query.filter_by(user_id = user_id).all()
    other_user_locations = Location.Location.query.filter(Location.Location.user_id != user_id, Location.Location.created_at >= datetime.today() - timedelta(days=14)).all()
    users_to_notify = set()
    for location in current_user_locations:
        current_latitude, current_longitude = location.latitude, location.longitude
        for location2 in other_user_locations:
            time_elapsed = abs(location2.created_at - location.created_at)
            if distance(current_latitude, current_longitude, location2.latitude, location2.longitude) <= 30 and time_elapsed.total_seconds() <= 600:
                users_to_notify.add(location2.user_id)

    if users_to_notify:
        push_to_email_queue(users_to_notify)

    return {"message": "success"}, 200

def push_to_email_queue(user_data):
    client = tasks.CloudTasksClient()

    project = environ.get('PROJECT_ID')
    location = environ.get('EMAIL_NOTIFICATION_QUEUE_LOCATION')
    email_queue = environ.get('EMAIL_NOTIFICATION_QUEUE')

    parent = client.queue_path(project, location, email_queue)

    for user in user_data:
        task = {
            'app_engine_http_request': {
                'http_method': 'POST',
                'relative_uri': '/send-email',
                'app_engine_routing': {
                    'service': 'email-notification-service'
                },
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'user_id': user}).encode()
            }
        }

        response = client.create_task(parent, task)
        print(response)



#Run Server
if __name__ == '__main__':
    app.run()