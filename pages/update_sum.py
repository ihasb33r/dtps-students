from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError
from datetime import datetime
from lib import update


class MainPage(webapp.RequestHandler):
    def get(self):
        update.updateSummary()


application = webapp.WSGIApplication(
                                     [('/updatesummary', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
