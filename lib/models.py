from google.appengine.ext import db


class Course(db.Model):
    name = db.StringProperty()
    cid = db.StringProperty()
    hasSeptemberResults = db.BooleanProperty(default=False)
    hasFebruaryResults = db.BooleanProperty(default=False)
    hasJuneResults = db.BooleanProperty(default=False)
    nTimesUpdated = db.IntegerProperty(default=0)
    added_june = db.DateTimeProperty()
    added_febr = db.DateTimeProperty()
    added_sept = db.DateTimeProperty()
    grades = db.TextProperty()

class Summary(db.Model):
    courses = db.TextProperty()

class Grade(db.Model):
    cname = db.StringProperty()
    cid = db.StringProperty()
    grade = db.StringProperty()
    sid = db.StringProperty()
    added_results_on = db.DateTimeProperty(auto_now=True)
    period = db.StringProperty()

    def asDict(self):
        return {"cid":self.cid, "name":self.cname, "grade":self.grade, "period":self.period, "added":unicode(self.added_results_on)}

class Settings(db.Model):
    period = db.IntegerProperty()
    default_num_of_updates = db.IntegerProperty(default=2)
    forced_updates = db.BooleanProperty(default=False)





