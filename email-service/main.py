from flask import Flask, request, jsonify
from __init__ import app, db, ma
from os import environ, path
from dotenv import load_dotenv
from flask_mail import Mail, Message

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'cloudcomp9768@gmail.com',
    "MAIL_PASSWORD": 'ccl_proj2'
}

app.config.update(mail_settings)
mail = Mail(app)


@app.route('/send-email', methods=['POST'])
def generate_notification():
    user_id = request.json['user_id']

    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=user_id,  # replace with your email for testing
                      body="Hi, \r\n You were in proximity of a person in the last 14 days who is currently infected from Cov-19 \r\n Please quarantine yourself and help protect others \r\n Thank you")
    mail.send(msg)
    return {"message": "success"}, 200



#Run Server
if __name__ == '__main__':
    app.run()