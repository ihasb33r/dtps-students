from google.appengine.ext import webapp
from google.appengine.ext import db
from lib.models import Course
import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError


class MainPage(webapp.RequestHandler):
    def get(self):

        course_id = self.request.get('id')
        if course_id == "":
            course_id = self.request.get('cid')
        json = self.request.get('json', default_value="false")
        query = db.GqlQuery("SELECT * FROM Course WHERE cid=:1",course_id )
        course = query.fetch(1)[0]
        if json=="false":
            path = os.path.join(os.path.dirname(__file__), '../templates/course.html')
            self.response.out.write(template.render(path, {"id":course_id, "name":course.name}))
        if json=="true":
            self.response.out.write(course.grades)
        

application = webapp.WSGIApplication(
                                     [('/course', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
