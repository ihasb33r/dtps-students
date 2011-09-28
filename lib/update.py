#coding: utf-8

import logging
from google.appengine.ext import db
from google.appengine.ext import deferred
from models import Course
from models import Summary
from models import Grade
import students_parser
from django.utils import simplejson
from datetime import datetime
import urllib
import urlparse
from socialpost import update_twitter

def encodekeyval(key, val):
    key = urllib.quote_plus(key)
    val = urllib.quote_plus(val)
    return key + '=' + val

def delete_grades(cid, period):
    grades  = db.GqlQuery("SELECT * FROM Grade WHERE cid=:1 AND period=:2", cid, period)
    db.delete(grades)


def add_grades(cid, period):
    course = db.GqlQuery("SELECT * FROM Course WHERE cid=:1", cid).fetch(1)[0]
    grades = simplejson.loads(course.grades)
    for grade in grades:
        new_grade = Grade()
        new_grade.cid = cid
        new_grade.cname = course.name
        new_grade.grade = grade["grade"]
        new_grade.sid = grade["sid"]
        new_grade.period = grade["period"]
        new_grade.put()



def updateSummary():

    logging.info("UPDATING SUMMARY")
    query = Summary.all()
    db.delete(query)
    courses = Course.all()
    items = []
    
    for course in courses:
        item = {}
        item['name'] = course.name
        item['id'] = course.cid
        item['hasSept'] = course.hasSeptemberResults
        item['hasFebr'] = course.hasFebruaryResults
        item['hasJune'] = course.hasJuneResults
        item['recent'] = course.nTimesUpdated
        item['addedJune'] = str(course.added_june)
        item['addedSept'] = str(course.added_sept)
        item['addedFebr'] = str(course.added_febr)
        items.append(item)
    
    summary = Summary()
    summary.courses = simplejson.dumps(items)
    summary.put()
    logging.info("FINISHED UPDATING SUMMARY")


def update(course, period):

    page = students_parser.get_course_page(course.cid)
    cname = students_parser.get_course_name(page)
    course.name = cname
    addgrades = False

    if students_parser.has_grades_for(page,period):
        grades_list= students_parser.get_grades_list(page)
        grades_json = simplejson.dumps(grades_list)

        addgrades = True
        course.grades = grades_json

        if period == u"ΦΕΒΡ":
            course.hasFebruaryResults=True
            course.added_febr = datetime.now()

        elif period == u"ΙΟΥΝ":
            course.hasJuneResults=True
            course.added_june = datetime.now()

        elif period == u"ΣΕΠΤ":
            course.hasSeptemberResults=True
            course.added_sept = datetime.now()


    course.nTimesUpdated = course.nTimesUpdated + 1
    course.put()

    if addgrades:
        deferred.defer(updateSummary)
        deferred.defer(update_twitter, course.name, course.cid)
        deferred.defer(delete_grades, course.cid, period)
        deferred.defer(add_grades, course.cid, period)
        logging.info("Updated course %s with grades" % (course.name))
    else:
        logging.info("Updated course %s without grades" % (course.name))




def run_update(num):
    february = 0
    june = 1 
    september = 2
    periods = [u"ΦΕΒΡ", u"ΙΟΥΝ", u"ΣΕΠΤ"]
    settings = db.GqlQuery("SELECT * FROM Settings").fetch(1)[0]
    if settings.period == february:
        query = db.GqlQuery("SELECT * FROM Course WHERE hasFebruaryResults=False ORDER BY nTimesUpdated ASC")
    elif settings.period == june:
        query = db.GqlQuery("SELECT * FROM Course WHERE hasFebruaryResults=False AND hasJuneResults=False ORDER BY nTimesUpdated ASC")
    elif settings.period == september:
        query = db.GqlQuery("SELECT * FROM Course WHERE hasSeptemberResults=False ORDER BY nTimesUpdated ASC")
    courses = query.fetch(num)
    items_updated = []
    for course in courses:
        update(course, periods[settings.period])
        items_updated.append(course)
    return items_updated

def is_time_to_update():
    return True;
