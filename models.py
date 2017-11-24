from flask import Flask
from __init__ import db , app




class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    counter = db.Column(db.Integer, default=0)
  
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def get_string(self):
        return unicode(self.username)

    def get_counter(self):
        return self.counter

    def __repr__(self):
        return '<User %r>' % self.username



    
