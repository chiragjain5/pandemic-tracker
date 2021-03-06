from datetime import datetime
from __init__ import db, ma
from marshmallow import  fields


class User(db.Model):
    # id = id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), index=False, unique=False, nullable=False)
    id = db.Column(db.String(50), primary_key=True)
    # mobile = db.Column(db.String(20), index=False, unique=False, nullable=True)
    # address = db.Column(db.String(200), index=False, unique=False, nullable=True)
    is_diseased = db.Column(db.Integer, index=False, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, id, is_diseased=False):
        # self.name = name
        self.id = id
        # self.mobile = mobile
        # self.address = address
        self.is_diseased = is_diseased
        # self.created_at = datetime.now()

    def __repr__(self):
        return '<User(name={self.id!r})>'.format(self=self)


class UserSchema(ma.Schema):
    id = fields.Str()
    created_at = fields.DateTime()
    status = fields.Method("format_diseased")

    def format_diseased(self, user):
        if user.is_diseased:
            return "infected"
        else:
            return "cured"
