from datetime import datetime
from __init__ import db, ma

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_type = db.Column(db.String(50), index=False, unique=False, nullable=False)
    status = db.Column(db.String(50), index=False, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    user = db.relationship('User', foreign_keys='Notification.user_id')

    def __init__(self, user_id, notification_type='EMAIL', status='PENDING'):
        self.user_id = user_id
        self.notification_type = notification_type
        self.status = status

    def __repr__(self):
        return '<Notification(name={self.user_id!r})>'.format(self=self)


class NotificationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'notification_type', 'status','created_at')