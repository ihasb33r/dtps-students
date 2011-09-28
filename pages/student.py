from google.appengine.ext import db
from lib.models import Course
from lib.models import Grade
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson
import os
import cgi

class MainPage(webapp.RequestHandler):
    def get(self):
        json = "false"

        json = self.request.get("json")
        sid = self.request.get('id')
        if sid == "":
            sid = self.request.get('sid')

        if json == "true":
            grades = Grade.all().filter("sid =", sid[-5:])
            gradelist = []
            for grade in grades:
                gradelist.append(grade.asDict())
            self.response.out.write(simplejson.dumps(gradelist))
        
        else:
            template_values = {
                    "title":cgi.escape(sid),
                    "id":cgi.escape(sid),
                    }
            path = os.path.join(os.path.dirname(__file__), '../templates/student.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/student', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
