from __init__ import db
from Models import User, Location, Notification

# Data to initialize database with
PEOPLE = [
    {'name': 'Doug', 'email': 'Farrell@yahoo.com', 'mobile': '1234567', 'address' : 'ABC DEF GHI'},
    {'name': 'Kent', 'email': 'Kent@yahoo.com', 'mobile': '123124532', 'address': 'XYZ DEF GFHI'},
    {'name': 'Bunny', 'email': 'Bunny@gmail.com', 'mobile': '12341353', 'address' : 'ASDASFD SAF ASF'}
]
LOCATIONS = [
    {'user_id' : 1, 'latitude' : 123.234, 'longitude' : 1234.45},
    {'user_id': 2, 'latitude': 113.234, 'longitude': 555.45},
    {'user_id': 3, 'latitude': 344.234, 'longitude': 22.45}
]
NOTIFICATION = [
    {'user_id': 1},
    {'user_id': 2},
    {'user_id': 3}
]


# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
# for person in PEOPLE:
#     p = User.User(name=person['name'], email=person['email'], mobile=person['mobile'], address=person['address'])
#     db.session.add(p)

# for location in LOCATIONS:
#     p = Location.Location(user_id=location['user_id'], latitude=location['latitude'], longitude=location['longitude'])
#     db.session.add(p)
# loc = Location.Location.query.all()
for notification in NOTIFICATION:
    p = Notification.Notification(user_id=notification['user_id'])
    db.session.add(p)
# loc = Location.Location.query.all()
# for l in loc:
#     print(l.user.name)
db.session.commit()
