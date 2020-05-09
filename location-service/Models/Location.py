from datetime import datetime
from __init__ import db, ma

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float(precision=32, decimal_return_scale=None), index=False, unique=False, nullable=False)
    longitude = db.Column(db.Float(precision=32, decimal_return_scale=None), index=False, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    user = db.relationship('User', foreign_keys='Location.user_id')

    def __init__(self, user_id, latitude, longitude):
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Location(name={self.user_id!r})>'.format(self=self)


class LocationSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'latitude', 'longitude', 'created_at')
