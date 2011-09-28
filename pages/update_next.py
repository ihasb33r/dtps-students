from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError
from datetime import datetime
from lib import update


class MainPage(webapp.RequestHandler):
    def get(self):

        number_of_courses = int(self.request.get('num', default_value="2"))
        if update.is_time_to_update():

            courses = update.run_update(number_of_courses)
            for course in courses:
                self.response.out.write("OK " + course.name + "<br />")
        else:
            self.response.out.write("not a good time")

application = webapp.WSGIApplication(
                                     [('/updatenext', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
