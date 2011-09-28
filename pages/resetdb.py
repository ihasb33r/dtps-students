from lib.models import Course
from lib.models import Summary
from google.appengine.ext import db
from lib import students_parser
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError


def delete_all():
    query  = Course.all()
    db.delete(query)

def reset():
    delete_all()
    course_list = students_parser.get_course_ids()

    for course_id in course_list:
        cname = course_id
        newCourse = Course()
        newCourse.cid = course_id
        newCourse.name = cname
        newCourse.put()

    db.delete(Summary().all())
    summary = Summary()
    summary.courses = ""
    summary.put()




class MainPage(webapp.RequestHandler):
    def get(self):
        try:
            reset()
        except DeadlineExceededError:
            pass
        self.response.out.write("OK")
application = webapp.WSGIApplication(
                                     [('/resetdb', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
 
