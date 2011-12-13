#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import os
import Cookie
import algaeModels

def deleteSession():
  thecookie = Cookie.SimpleCookie()
  cookie_string = os.environ.get('HTTP_COOKIE')
  if cookie_string:
    thecookie.load(cookie_string)
    sessionQuery = db.GqlQuery("SELECT * FROM userSession WHERE sessionID = '" + thecookie['session'].value + "'")
    session = sessionQuery.get()
    if session:
      session.delete()
      return True
  return False

sessionDeleted = deleteSession()
thiscookie = Cookie.SimpleCookie()

thiscookie['session'] = "0"
thiscookie['username'] = "noUser"
print thiscookie
if sessionDeleted:
  print "Location: admin?logout=sucess"
else:
  print "Location: admin?logout=failure"
print 'Content-Type: text/html\n'
