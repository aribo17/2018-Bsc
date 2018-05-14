# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
#from app import Base
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from json import JSONEncoder
import time
from sqlalchemy import Column, Integer, String,SmallInteger, Boolean, DateTime, Time, Date, ForeignKey, Float, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


# Define a base model for other database tables to inherit
class BaseTable(db.Model):
    __abstract__  = True

    id            = Column(Integer, primary_key=True)
    date_created  = Column(DateTime,  default=func.current_timestamp())
    date_modified = Column(DateTime,  default=func.current_timestamp(),
                                           onupdate=func.current_timestamp())


# Define a User model
class User(BaseTable):

    __tablename__ = 'users'

    # User Name
    name = Column(String(80))
    phone = Column(Integer)
    company = Column(String(80))

    # Identification Data: email & password
    email = Column(String(128),  nullable=False, unique=True)
    password = Column(String(192),  nullable=False)

    # Authorisation Data: role & status
    role = Column(SmallInteger, nullable=False)
    event_created = relationship("Event", back_populates='owner')

    # New instance instantiation procedure
    def __init__(self, name, phone, email, password, company, role):

        self.name = name
        self.phone = phone
        self.email = email
        self.password = generate_password_hash(password)
        self.company = company
        self.role = role

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '%r,%r,%r' % (self.name, self.phone, self.email)


class Event(BaseTable):
    __tablename__ = 'events'
    owner_name = Column(String(80))
    owner_id = Column(String(80), ForeignKey('users.id'))
    name = Column(String(80))
    type = Column(String(80))
    category = Column(Integer)
    description = Column(String(1000))
    updated_time = Column(DateTime)
    startDate = Column(Date)
    startTime = Column(Time)
    endDate = Column(Date)
    endTime = Column(Time)
    canceled = Column(Boolean)
    attending_count = Column(Integer)
    maybe_count = Column(Integer)
    declined_count = Column(Integer)
    future_event = Column(Boolean)
    photo = Column(String)
    deleted = Column(Boolean, default=False)
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", back_populates='event')
    owner = relationship("User", back_populates='event_created')

    def __init__(self, location_id, owner_name, name, type, category, description, startDate, startTime, endDate, endTime, photo, deleted):
        self.location_id = location_id
        self.owner_name = owner_name
        self.name = name
        self.type = type
        self.category = category
        self.description = description
        self.startDate = startDate
        self.startTime = startTime
        self.endDate = endDate
        self.endTime = endTime
        self.photo = photo
        self.deleted = deleted

    def format_date(obj):
        if not obj:
            return obj.strftime('%Y-%m-%d')

    def format_time(obj):
        if not obj:
            return obj.strftime('%H-%M-%S')

    def __repr__(self):
        return '%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r' % (self.location_id, self.owner_name, self.name, self.type, self.description, self.category,
                                                     self.startDate, self.startTime, self.endDate, self.endTime, self.photo)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'type': self.type,
           'description':self.description,
           'category': self.category,
           'startDate':dump_datetime(self.startDate),
           'startTime': dump_datetime(self.startTime),
           'endData':dump_datetime(self.endDate),
           'endTime':dump_datetime(self.endTime),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }


class Location(BaseTable):

    __tablename__ = 'location'

    name = Column(String(80))
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String(80))
    city = Column(String(80))
    street = Column(String(80))
    zip_code = Column(Integer)
    event = relationship("Event", back_populates='location')

    def __init__(self, name, latitude, longitude, country, city, street, zip_code):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        self.city = city
        self.street = street
        self.zip_code = zip_code

    def __repr__(self):
        return '%r,%r,%r,%r,%r,%r,%r' % (self.name, self.latitude, self.longitude, self.country, self.city, self.street, self.zip_code)


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                'name': obj.name,
                'type': obj.type,
                'description': obj.description,
                'category': obj.category,
                'startDate': obj.startDate.strftime('%Y-%m-%d'),
                'startTime': obj.startTime.strftime('%H:%M:%S'),
                'endDate': obj.endDate.strftime('%Y-%m-%d'),
                'endTime': obj.endTime.strftime('%H:%M:%S'),
                'photo': obj.photo,
                'deleted': obj.deleted
            }
        if isinstance(obj, Location):
            return {
                'name': obj.name,
                'latitude': obj.latitude,
                'longitude': obj.longitude,
                'country': obj.country,
                'city': obj.city,
                'street': obj.street,
                'zip_code': obj.zip_code,
                'event': obj.event,
            }
        return super(MyJSONEncoder, self).default(obj)
