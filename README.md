RegisterBot
===========

Texts you when spaces become available at your chosen UIUC classes.


First off, you will need python 2
http://www.python.org/download/releases/2.7.6/


You will next need to install lxml. The binaries are available at:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

If you have 32 bit python 2.7, install "lxml-3.2.4.win32-py2.7.exe" (ctrl+f lxml should do the trick)

Next, you will need to open command line. Easiest way to do so:
```
windows key +r
type in "cmd"
click enter
```

then, in the command line that pops up, run the following commands:

```
cd "C:\Python27\Scripts"
easy_install pip
pip install pyquery
pip install twilio
pip install mechanize
```
Next, you will need a twilio account (that enables texting)
https://www.twilio.com/try-twilio

The twilio account will have an account_sid and auth_token which you will need
to set up below. It will also have a phone number. This is your "fromnum".

The "tonum" variable is your telephone number (yes, the + is needed, and it
starts with 1 and your area code)

Lastly, you will need the CRNs for the courses you are waiting for. This is an array, given in "courses".

All of these settings are at the top of the python file.


And no, this does not work on python 3.
