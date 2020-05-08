from datetime import datetime
from __init__ import db, ma


class User(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), index=False, unique=False, nullable=False)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    # mobile = db.Column(db.String(20), index=False, unique=False, nullable=True)
    # address = db.Column(db.String(200), index=False, unique=False, nullable=True)
    is_diseased = db.Column(db.Integer, index=False, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, name, email, address=None, mobile=None, is_diseased=False):
        # self.name = name
        self.email = email
        # self.mobile = mobile
        # self.address = address
        self.is_diseased = is_diseased
        # self.created_at = datetime.now()

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class UserSchema(ma.Schema):
    class Meta:
        # fields = ('id', 'name', 'email', 'mobile', 'address', 'is_diseased', 'created_at')
        fields = ('id', 'email', 'is_diseased', 'created_at')
