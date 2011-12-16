#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import cgi
import Cookie
import hashlib
import os
import re
import markdown2
import algaeModels
import algaePython
import algaeUserConfig

form = cgi.FieldStorage()
contentType = form["contentType"].value

thiscookie = Cookie.SimpleCookie()
cookie_string = os.environ.get('HTTP_COOKIE')
if not cookie_string:
	print "Location: admin?bad=cookie"
	print 'Content-Type: text/html\n'
else:
	thiscookie.load(cookie_string)

if contentType == "blogPost" or contentType == "basicPage":
	postID = form.getfirst("postID", "none")
	if contentType == "blogPost":
		if postID == "none":
			thePost = algaeModels.blogPost()
		else:
			thePost = algaeModels.blogPost.get(postID)
	else:
		if postID == "none":
			thePost = algaeModels.basicPage()
		else:
			thePost = algaeModels.basicPage.get(postID)
	thePost.author = thiscookie['username'].value
	theTitle = form.getfirst("postTitle", "Untitled").decode( 'utf-8', 'ignore')
	thePost.postTitle = theTitle
	url = re.sub(r'[- ]', "_", theTitle)
	url = re.sub(r'\W', "", url)
	url = re.sub(r'_+', "-", url)
	if url != thePost.cleanURL:
	  url = algaePython.noDupeURL(url, contentType)
	thePost.cleanURL = url
	if contentType == "blogPost":
		extLink = form.getfirst("linkURL", "null").decode( 'utf-8', 'ignore')
		thePost.linkURL = extLink
	thePost.postText = db.Text(form.getfirst("postText", ""), encoding="utf-8")
	thePost.markdownText = db.Text(markdown2.markdown(form.getfirst("postText", ""))) #, encoding="utf-8" as 2nd argument of db.Text if not already unicode
	if form.getfirst("isPublished", "False") == "on":
		thePost.isPublished = True
	else:
		thePost.isPublished = False
	thePost.put()
	if contentType == "blogPost":
		print "Location: admin?saved=yes&edit=blogPost&key=" + str(thePost.key())
	else:
		print "Location: admin?saved=yes&edit=basicPage&key=" + str(thePost.key())
	print 'Content-Type: text/html\n'
elif contentType == 'navLink':
  postID = form.getfirst("postID", "none")
  if postID == "none":
    theNav = algaeModels.navLink()
    countQuery = db.GqlQuery("SELECT * FROM navLink")
    theNav.rank = countQuery.count()
  else:
		theNav = algaeModels.navLink.get(postID)
  theNav.postTitle = form.getfirst("postTitle", "No Link").decode( 'utf-8', 'ignore')
  theNav.altText = form.getfirst("altText", "").decode( 'utf-8', 'ignore')
  theNav.theLink = form.getfirst("theLink", "#").decode( 'utf-8', 'ignore')
  theNav.put()
  print "Location: admin?saved=yes&edit=navLink"
  print 'Content-Type: text/html\n'
elif contentType == 'navOrder':
  postID = form.getfirst("key", "none")
  if postID != "none":
    theNav = algaeModels.navLink.get(postID)
    theRank = theNav.rank
    if form.getfirst("direction", "none") == 'up':
    	navQuery = db.GqlQuery("SELECT * FROM navLink WHERE rank=" + str(theRank - 1))
    	otherNav = navQuery.get()
    	theNav.rank = theRank - 1
    	otherNav.rank = theRank
    	theNav.put()
    	otherNav.put()
    elif form.getfirst("direction", "none") == 'down':
    	navQuery = db.GqlQuery("SELECT * FROM navLink WHERE rank=" + str(theRank + 1))
    	otherNav = navQuery.get()
    	theNav.rank = theRank + 1
    	otherNav.rank = theRank
    	theNav.put()
    	otherNav.put()
  print "Location: admin?saved=yes&edit=navLink"
  print 'Content-Type: text/html\n'
elif contentType == 'siteUser':
  postID = form.getfirst("postID", "none")
  if postID == "none":
    theUser = algaeModels.siteUser()
  else:
		theUser = algaeModels.siteUser.get(postID)
  theUser.userName = form.getfirst("userName", "nobody").decode( 'utf-8', 'ignore')
  theUser.displayName = form.getfirst("displayName", "Nobody").decode( 'utf-8', 'ignore')
  theUser.userEmail = form.getfirst("userEmail", "nobody@nothing.com").decode( 'utf-8', 'ignore')
  theUser.role = form.getfirst("role", "author")
  theUser.saltedPwd = hashlib.md5(form.getfirst("pWord", "badPassword") + algaeUserConfig.passSalt).hexdigest()
  theUser.put()
  print "Location: admin?saved=yes&edit=siteUser"
  print 'Content-Type: text/html\n'
elif contentType == "styleSheet" or contentType == "jScript":
	postID = form.getfirst("postID", "none")
	if contentType == "styleSheet":
		if postID == "none":
			thePost = algaeModels.styleSheet()
		else:
			thePost = algaeModels.styleSheet.get(postID)
	else:
		if postID == "none":
			thePost = algaeModels.jScript()
		else:
			thePost = algaeModels.jScript.get(postID)
	theTitle = form.getfirst("postTitle", "Untitled").decode( 'utf-8', 'ignore')
	thePost.postTitle = theTitle
	url = re.sub(r' ', "_", theTitle)
	url = re.sub(r'\W', "", url)
	url = re.sub(r'_+', "-", url)
	if url != thePost.cleanURL:
	  url = algaePython.noDupeURL(url, contentType)
	thePost.cleanURL = url
	thePost.postText = db.Text(form.getfirst("postText", ""), encoding="utf-8")
	if form.getfirst("isPublished", "False") == "on":
		thePost.isPublished = True
	else:
		thePost.isPublished = False
	thePost.put()
	if contentType == "styleSheet":
		print "Location: admin?saved=yes&edit=styleSheet&key=" + str(thePost.key())
	else:
		print "Location: admin?saved=yes&edit=jScript&key=" + str(thePost.key())
	print 'Content-Type: text/html\n'
elif contentType == 'delete':
	postID = form.getfirst("postID", "none")
	cType = form.getfirst("cType", "none")
	if postID != "none" and cType != "none":
		if cType == 'blogPost':
			theContent = algaeModels.blogPost.get(postID)
		elif cType == 'basicPage':
			theContent = algaeModels.basicPage.get(postID)
		elif cType == 'navLink':
			theContent = algaeModels.navLink.get(postID)
		elif cType == 'styleSheet':
			theContent = algaeModels.siteUser.get(postID)
		elif cType == 'jScript':
			theContent = algaeModels.basicPage.get(postID)
		if theContent:
			theContent.delete()
	print "Location: admin?deleted=yes&edit=" + cType
	print 'Content-Type: text/html\n'
else:
	print "Location: admin"
	print 'Content-Type: text/html\n'