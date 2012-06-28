#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import datetime
from model import Entry
from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(
		os.path.join(os.path.dirname(__file__), 'template')))

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	template_values = {
    		'date': datetime.datetime.today().strftime("%Y-%m-%d")
    	}
        q = db.GqlQuery('SELECT * FROM Entry')
        template_values['count'] = q.count()

        entries = db.GqlQuery('SELECT * FROM Entry LIMIT 10')
        template_values['entries'] = entries

        user = users.get_current_user()
        if user:
            template_values['user'] = user.nickname()
            template_values['logout_url'] = users.create_logout_url('/')
        else:
            template_values['login_url'] = users.create_login_url()

    	template = jinja_environment.get_template("index.html")
    	self.response.out.write(template.render(template_values))
        #self.response.out.write('Hello world!')

class AddEntryHandler(webapp2.RequestHandler):
    def post(self):
        target = self.request.get('target')
        amount = int(self.request.get('amount'))
        date = datetime.datetime.strptime(self.request.get('date'), '%Y-%m-%d').date()
        succeed = True#self.request.get('succeed')
        story = self.request.get('story')
         
        entry = Entry(target=target, amount=amount, date=date, succeed=succeed, story=story, author=users.get_current_user())
        entry.put()

        self.redirect('/')


app = webapp2.WSGIApplication([
            ('/', MainHandler),
            ('/add_entry', AddEntryHandler)
        ],
        debug=True)
