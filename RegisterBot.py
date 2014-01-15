"""
First off, you will need python 2
http://www.python.org/download/releases/2.7.6/


You will next need to install lxml. The binaries are available at:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

If you have 32 bit python 2.7, install "lxml-3.2.4.win32-py2.7.exe" (ctrl+f lxml should do the trick)

Next, you will need to open command line. Easiest way to do so:
<windows key>+r
type in cmd
click enter

then, in the command line that pops up, run the following commands:

cd "C:\Python27\Scripts"
easy_install pip
pip install pyquery
pip install twilio
pip install mechanize

Next, you will need a twilio account (that enables texting)
https://www.twilio.com/try-twilio

The twilio account will have an account_sid and auth_token which you will need
to set up below. It will also have a phone number. This is your "fromnum".

The "tonum" variable is your telephone number (yes, the + is needed, and it
starts with 1 and your area code)

Lastly, you will need the CRNs for the courses you are waiting for. This 
"""


account_sid = "AG854<some stuff here>47f9bad4"
auth_token = "b5qced<AUTH TOKEN HERE>6gef70f2"
tonum = "+12170123456"      #Your cellphone number
fromnum =  "+12170123456" #Your twilio number
#A list of the CRNs of each class
courses = [31423,36149,36782]
waittime=60*60   #It checks every hour



"""
Mechanize is used, so that it is easy to later add automatic registration.
The login function logs you in to enterprise. All that is now necessary is
the actual automatic registration code...
"""


from pyquery import PyQuery as pq
import mechanize
import cookielib
import re
import getpass
import twilio
import time
from twilio.rest import TwilioRestClient


try:
    client = twilio.rest.TwilioRestClient(account_sid, auth_token)
except twilio.TwilioRestException as e:
    print e


def login(br):
    print "ENTERPRISE LOGIN:"
    eid = raw_input("Enterprise ID: ")
    passwd = getpass.getpass()

    print "LOGGING IN"
    br.open('https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1')

    # Select the second (index one) form - the first form is a search query box
    br.select_form(nr=0)

    # User credentials
    br.form['inputEnterpriseId'] = eid
    br.form['password'] = passwd

    # Login
    response = br.submit()
    print "LOGIN COMPLETE"

def getCourse(browser,crn):
    response = browser.open("https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120141&crn_in="+str(crn))

    cls = pq(response.read())("table.datadisplaytable tr")
    #print pq(cls[0]).text()
    result = {}
    result["description"] = pq(cls[0]).text()
    try:
        result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),int(pq(pq(cls[5])("td")[0]).text())]
        result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),int(pq(pq(cls[5])("td")[1]).text())]
        result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),int(pq(pq(cls[5])("td")[2]).text())]
    except:
        result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),1]
        result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),1]
        result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),1]
    return result

#Set booleans for each course: Are seats available?
available = [False]*len(courses)

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Chrome')]

while (True):
    print "----------------------------------"
    for i in xrange(len(courses)):
        crn = courses[i]
        res = getCourse(br,crn)
        print res["description"],
        x = res["remaining"]
        if (x[0] > 0 and x[1] > 0):
            
            if (available[i]):
                 print ": seats available"
            else:
                print ": SEATS AVAILABLE"
                print "\tSending SMS"
                message = client.sms.messages.create(
                    body="SEATS AVAILABLE: "+res["description"],
                    to=tonum,
                    from_=fromnum
                )
                available[i]=True
        
        else:
            if (available[i]):
                print ": NO SEATS AVAILABLE"
                print "\tSending SMS"
                message = client.sms.messages.create(
                    body="NOT AVAILABLE: "+res["description"],
                    to=tonum,
                    from_=fromnum
                )
                available[i]=False
            else:
                print ": no seats available"
    time.sleep(waittime)
"""
#br.follow_link(text_regex=r"I Agree")
for link in br.links():
    print link.text, link.url

print ">Registration & Records"
br.follow_link(text_regex=r"Registration")
print ">Registration"
br.follow_link(text="Registration")
for link in br.links():
    print link.text, link.url
"""