#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
from google.appengine.api import images
import cgi
import Cookie
import hashlib
import os
import re
import markdown2
import algaeModels
import algaePython
import algaeUserConfig

def editPostOrPage(contentType, form, thiscookie):
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

def editNavLink(form):
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

def editNavOrder(form):
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

def editSiteUser(form):
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

def editCssOrJs(contentType, form):
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

def editImage(form):
  postID = form.getfirst("postID", "none")
  if postID == "none":
    thePost = algaeModels.algaeImage()
  else:
    thePost = algaeModels.algaeImage.get(postID)
  theTitle = form.getfirst("postTitle", "Untitled").decode( 'utf-8', 'ignore')
  thePost.postTitle = theTitle
  url = re.sub(r' ', "_", theTitle)
  url = re.sub(r'\W', "", url)
  url = re.sub(r'_+', "-", url)
  if url != thePost.cleanURL:
    url = algaePython.noDupeURL(url, 'algaeImage')
  thePost.cleanURL = url
  theImage = form.getfirst("img", "")
  thePost.imgData = db.Blob(theImage)
  smImage = images.resize(theImage, 32, 32)
  thePost.smData = db.Blob(smImage)
  mdImage = images.resize(theImage, 200, 200)
  thePost.mdData = db.Blob(mdImage)
  if form.getfirst("isPublished", "False") == "on":
    thePost.isPublished = True
  else:
    thePost.isPublished = False
  thePost.put()
  print "Location: admin?saved=yes&edit=image&key=" + str(thePost.key())
  print 'Content-Type: text/html\n'

def deleteContent(form):
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
			theContent = algaeModels.styleSheet.get(postID)
		elif cType == 'jScript':
			theContent = algaeModels.jScript.get(postID)
		if theContent:
			theContent.delete()
	print "Location: admin?deleted=yes&edit=" + cType
	print 'Content-Type: text/html\n'

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
  editPostOrPage(contentType, form, thiscookie)
elif contentType == 'image':
  editImage(form)
elif contentType == 'navLink':
  editNavLink(form)
elif contentType == 'navOrder':
  editNavOrder(form)
elif contentType == 'siteUser':
  editSiteUser(form)
elif contentType == "styleSheet" or contentType == "jScript":
  editCssOrJs(contentType, form)
elif contentType == 'delete':
  deleteContent(form)
else:
	print "Location: admin"
	print 'Content-Type: text/html\n'