#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

import Cookie
import cgi
import hashlib
import algaeModels
import algaePython
import algaeUserConfig
import datetime

form = cgi.FieldStorage()
loginUser = str(form["userName"].value)
loginPass = str(form["password"].value)

thiscookie = Cookie.SimpleCookie()

if algaePython.verifiedUser(loginUser):
	if algaePython.verifiedPassword(loginUser, loginPass):
		thiscookie['username'] = loginUser
		theSession = algaeModels.userSession()
		theSession.sessionUserName = loginUser
		#theSession.sessionExpires = figureThisShitOut
		mySessionID = hashlib.md5(loginUser + algaeUserConfig.passSalt + str(datetime.datetime.now())).hexdigest()
		theSession.sessionID = mySessionID
		theSession.put()
		thiscookie['session'] = mySessionID
		print thiscookie
		print "Location: admin"
		print 'Content-Type: text/html\n'
	else:
		print "Location: admin?bad=password"
		print 'Content-Type: text/html\n'
else:
	print "Location: admin?bad=user"
	print 'Content-Type: text/html\n'