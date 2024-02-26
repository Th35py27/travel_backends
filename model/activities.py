""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _family = db.Column(db.Boolean, nullable=False)
    _adult = db.Column(db.Boolean, nullable=False)
    _indoors = db.Column(db.Boolean, nullable=False)
    _outdoors = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, family, adult, indoors, outdoors):
        self._name = name
        self._family = family
        self._adult = adult
        self._indoors = indoors
        self._outdoors = outdoors

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def family(self):
        return self._family
    
    @family.setter
    def family(self, family):
        self._family = family
    
    @property
    def adult(self):
        return self._adult
    
    @adult.setter
    def adult(self, adult):
        self._adult = adult
    
    @property
    def indoors(self):
        return self._indoors
    
    @indoors.setter
    def indoors(self, indoors):
        self._indoors = indoors
    
    @property
    def outdoors(self):
        return self._outdoors
    
    @outdoors.setter
    def outdoors(self, outdoors):
        self._outdoors = outdoors
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "family": self.family,
            "adult": self.adult,
            "indoors": self.indoors,
            "outdoors": self.outdoors
        }

def initActivities():
    with app.app_context():
        db.create_all()
        activities = [
            Activity(name='San Diego Zoo', family=True, adult=True, indoors=False, outdoors=True),
            Activity(name='San Diego Safari Park', family=True, adult=True, indoors=False, outdoors=True),
            Activity(name='Sea World', family=True, adult=True, indoors=False, outdoors=True),
            Activity(name='La Jolla Beach', family=True, adult=True, indoors=False, outdoors=True),
            Activity(name='Torrey Pines Beach', family=True, adult=True, indoors=False, outdoors=True),
            Activity(name='Balboa Park', family=True, adult=True, indoors=True, outdoors=True),
            Activity(name='Old Town San Diego State Historic Park', family=True, adult=True, indoors=True, outdoors=True),
            Activity(name='USS Midway Museum', family=True, adult=True, indoors=True, outdoors=False),
            Activity(name='San Diego Museum of Art', family=True, adult=True, indoors=True, outdoors=False),
            Activity(name='San Diego Air & Space Museum', family=True, adult=True, indoors=True, outdoors=False),
            Activity(name='Gaslamp Quarter', family=False, adult=True, indoors=True, outdoors=True),
            Activity(name='San Diego Childrens Discovery Museum', family=True, adult=False, indoors=True, outdoors=False),
            Activity(name='Birch Aquarium at Scripps', family=True, adult=True, indoors=True, outdoors=False),
            Activity(name='San Diego Natural History Museum', family=True, adult=True, indoors=True, outdoors=False),
        ]
        for activity in activities:
            try:
                activity.create()
            except IntegrityError:
                db.session.rollback()
                print(f"Record exists")

