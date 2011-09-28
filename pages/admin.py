#coding: utf-8
from lib.models import Settings
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError
from google.appengine.ext.webapp import template
import os
import cgi


class MainPage(webapp.RequestHandler):
    def get(self):
        template_values={"title":"admin"}

        path = os.path.join(os.path.dirname(__file__), '../templates/admin.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        query = db.GqlQuery("SELECT * FROM Settings")
        settings = query.fetch(1)
        db.delete(settings)

        newsettings = Settings()
        period = self.request.get('period')

        if period =="1" :
            newsettings.period = 1
        if period =="2" :
            newsettings.period = 0
        if period =="3" :
            newsettings.period = 2 

        template_values={"title":"admin",
                "result":"ok"}
        newsettings.put()
        path = os.path.join(os.path.dirname(__file__), '../templates/admin.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/admin', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
 
