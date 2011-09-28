#coding:utf-8

from google.appengine.ext import db
from lib.models import Summary
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.api import memcache
from google.appengine.api import users
from django.utils import simplejson

class MainPage(webapp.RequestHandler):
    def get(self):
        json = self.request.get("json", default_value="false")

        courses = Summary.all().fetch(1)[0].courses
#        self.response.out.write(courses)
        if json=="false":
            path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
            self.response.out.write(template.render(path, {}))
        if json=="true":
            self.response.out.write(courses)
 
application = webapp.WSGIApplication(
                                     [('/', MainPage),('/main', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
