from flask import Flask, request, jsonify
from __init__ import app, db, ma
from Models import User
from google.cloud import tasks
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

db.create_all()


@app.route('/new-user', methods=['POST'])
def add_user():
    # name = request.json['name']
    id = request.json['user_id']
    # address = request.json['address']
    # mobile = request.json['mobile']
    exists = User.User.query.get(id)
    if not exists:
        new_user = User.User(id=id)
        db.session.add(new_user)
        db.session.commit()
        message = "Successfully created user: {}".format(id)
        user_schema = User.UserSchema()
        data = user_schema.dump(new_user)
        data['message'] = message
        return data, 201
    else:
        user_schema = User.UserSchema()
        data = user_schema.dump(exists)
        data['message'] = "User is already in the database"
        return data, 200


@app.route('/check-status', methods=['POST'])
def check_status():
    # name = request.json['name']
    # address = request.json['address']
    # mobile = request.json['mobile']
    id = request.json['user_id']
    user = User.User.query.get(id)
    if user:
        user_schema = User.UserSchema()
        return user_schema.jsonify(user)

    return {"message": "User doesn't exist in database"}, 404


@app.route('/update-infection', methods=['POST'])
def update_infection():
    # name = request.json['name']
    # address = request.json['address']
    # mobile = request.json['mobile']
    id = request.json['user_id']
    status = request.json['status']
    is_diseased = True if (status and status.lower() == "infected") else False
    user = User.User.query.get(id)
    if not user:
        return {"message": "User doesn't exist in database"}, 404

    user.is_diseased = is_diseased
    db.session.commit()
    send_to_queue(id)
    user_schema = User.UserSchema()
    data = user_schema.dump(user)
    data['message'] = "User infection status updated"
    return data, 200
    # if is_diseased:

def send_to_queue(user):
    client = tasks.CloudTasksClient()

    project = environ.get('PROJECT_ID')
    location = environ.get('NOTIFICATION_QUEUE_LOCATION')
    notification_queue = environ.get('NOTIFICATION_QUEUE')

    parent = client.queue_path(project, location, notification_queue)
    task = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': '/generate-notification',
            'app_engine_routing': {
                'service': 'notification-service'
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
