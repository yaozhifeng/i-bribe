#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import users

class Entry(db.Model):
	target = db.StringProperty(required=True, indexed=True)
	amount = db.IntegerProperty(required=True, default=100)
	date = db.DateProperty(auto_now_add=True, indexed=True)
	succeed = db.BooleanProperty(default=False, indexed=True)
	story = db.TextProperty()
	author = db.UserProperty(required=False)
