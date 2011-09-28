#coding: utf-8
import re
import urllib, urllib2, cookielib 
import logging

strip_tags = re.compile(r"<.*?>")
strip_nbsp = re.compile(r"&nbsp;")
empty_page_re = re.compile(unicode("δεν είναι διαθέσιμη","utf-8"))




def get_course_page(cid):
    """Download the page with the corresponding cid"""

    try:
        page_link = """http://students.unipi.gr/courseRelults.asp?dpcID=&orID=&mnuID=mnu5&studpg=&prID=&courseID="""+cid
        f = urllib2.urlopen( page_link )
        page = unicode(f.read(), "iso-8859-7")
    except:
        logging.error("Error while Downloading page for cid %s" % (cid))
        page = " "

    return page




def has_grades_for(input_page, period):
    """ Check if page has grades for given period """

    period_re = re.compile(period)
    page = unicode(input_page)
    result = period_re.search(page)

    if result!=None:
        return True
    else:
        return False


def get_course_ids(department_id="119"):
    courseid_re = re.compile("courseID=\d{8}")
    params = urllib.urlencode(dict( dID=department_id))
    courselist_page = urllib2.urlopen("""http://students.unipi.gr/courselist.asp?mnuid=mnu5&""", params).read()

    results = courseid_re.findall(courselist_page)
    ids = []
    for result in results:
         ids.append(result[-8:])

    return ids




def get_grades_list(page):
    tr_useless = re.compile("<td align=\"left\">.*?</td>")
    page = tr_useless.subn("", page)[0]

    td_re = re.compile("<td.*?valign=\"top\">[E\d{5}|\d{1,2}|\W{4}].*?</td>")
    lines = td_re.findall(page)
    item_keys = ["sid", "grade", "period"]
    counter=0
    item = {}
    grades_list = []
    
    for line in lines:
        item[item_keys[counter]]=strip_tags.subn("",line)[0]
        counter+=1
        if counter==3:
            counter = 0
            item[item_keys[counter]]=item[item_keys[counter]][-5:]
            grades_list.append(item)
            item={}
       
    return grades_list
        




def get_course_name(page):
    namediv_re = re.compile(r"""<div class="tablebold">.*?\(.*?\).*?</div>""", re.S)
    namediv = namediv_re.findall(page)
    notags = strip_tags.subn("",namediv[0])[0]
    nonbsp = strip_nbsp.subn(" ", notags)[0]
    name =  ' '.join(nonbsp.split("-")[:-1])
    return name
