#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import cgi
import datetime
from pytz.gae import pytz
import algaeUserConfig

class siteUser(db.Model):
  userName = db.StringProperty()
  displayName = db.StringProperty()
  saltedPwd = db.StringProperty()
  userEmail = db.EmailProperty()
  role = db.StringProperty()
  
  def __repr__(self):
    return self.userName

  def __str__(self):
    return self.userName

  def canEditType(self, contentType):
    if self.role == 'admin':
      return True
    elif self.role == 'author':
      if contentType == 'blogPost' or contentType == 'basicPage':
        return True
    elif self.role == 'designer':
      if contentType == 'styleSheet' or contentType == 'jScript':
        return True
    return False

class userSession(db.Model):
	sessionID = db.StringProperty()
	sessionUserName = db.StringProperty()
	
	def __repr__(self):
		return self.sessionID

	def __str__(self):
		return self.sessionID

class blogPost(db.Model):
  author = db.StringProperty()
  postTime = db.DateTimeProperty(auto_now_add=True)
  postTitle = db.StringProperty()
  cleanURL = db.StringProperty()
  linkURL = db.StringProperty()
  postText = db.TextProperty()
  markdownText = db.TextProperty()
  isPublished = db.BooleanProperty()
  
  def __repr__(self):
    return self.postTitle

  def __str__(self):
    return self.postTitle
	
  def dateTimeString(self):
    siteTZ = pytz.timezone(algaeUserConfig.siteTimeZone)
    localDT = self.postTime.replace(tzinfo=pytz.utc).astimezone(siteTZ)
    myDT = ""
    myDT += str(localDT.month)
    myDT += '/' + str(localDT.day)
    myDT += '/' + str(localDT.year)
    myDT += ' at '
    pm = False
    myHour = localDT.hour
    if myHour >= 12:
      pm = True
      myHour -= 12
    if myHour == 0:
      myHour = 12
    myDT += str(myHour)
    if len(str(localDT.minute)) == 1:
      myDT += ':0' + str(localDT.minute)
    else:
      myDT += ':' + str(localDT.minute)
    if pm:
      myDT += ' PM'
    else:
      myDT += ' AM'
    return myDT

  def printArticle(self, link=True):
    print '<article>'
    print '<header>'
    authorQuery = db.GqlQuery("SELECT * FROM siteUser WHERE userName = '" + self.author + "'")
    author = authorQuery.get()
    if self.linkURL != 'null':
      print '<h1><a href="' + cgi.escape(self.linkURL.encode('utf-8')) + '">' + cgi.escape(self.postTitle.encode('utf-8')) + '</a></h1>'
      print "<p>posted by: " + cgi.escape(author.displayName.encode('utf-8')) + " on " + self.dateTimeString() + " " + '<a href="/posts/' + cgi.escape(self.cleanURL.encode('utf-8')) + '">&infin;</a>' + "</p>"
    elif link:
      print '<h1><a href="/posts/' + cgi.escape(self.cleanURL.encode('utf-8')) + '">' + cgi.escape(self.postTitle.encode('utf-8')) + '</a></h1>'
      print "<p>posted by: " + cgi.escape(author.displayName.encode('utf-8')) + " on " + self.dateTimeString() + " " + '<a href="/posts/' + cgi.escape(self.cleanURL.encode('utf-8')) + '">&infin;</a>' + "</p>"
    else:
      print "<h1>" + cgi.escape(self.postTitle.encode('utf-8')) + "</h1>"
      print "<p>posted by: " + cgi.escape(author.displayName.encode('utf-8')) + " on " + self.dateTimeString() + "</p>"
    print '</header>'
    print self.markdownText.encode('utf-8')
    print '</article>'
  
  def linkUrl(self):
    if self.linkURL == 'null':
      return ''
    else:
      return self.linkURL

class basicPage(db.Model):
	author = db.StringProperty()
	postTime = db.DateTimeProperty(auto_now_add=True)
	postTitle = db.StringProperty()
	postText = db.TextProperty()
	markdownText = db.TextProperty()
	cleanURL = db.StringProperty()
	isPublished = db.BooleanProperty()

	def __repr__(self):
		return self.postTitle.encode('utf-8')

	def __str__(self):
		return self.postTitle.encode('utf-8')

class navLink(db.Model):
	postTitle = db.StringProperty()
	altText = db.StringProperty()
	theLink = db.StringProperty()
	rank = db.IntegerProperty()

	def __repr__(self):
		return self.postTitle

	def __str__(self):
		return self.postTitle

class styleSheet(db.Model):
	postTime = db.DateTimeProperty(auto_now_add=True)
	postTitle = db.StringProperty()
	postText = db.TextProperty()
	cleanURL = db.StringProperty()
	isPublished = db.BooleanProperty()

	def __repr__(self):
		return self.postTitle

	def __str__(self):
		return self.postTitle

class jScript(db.Model):
	postTime = db.DateTimeProperty(auto_now_add=True)
	postTitle = db.StringProperty()
	postText = db.TextProperty()
	cleanURL = db.StringProperty()
	isPublished = db.BooleanProperty()

	def __repr__(self):
		return self.postTitle

	def __str__(self):
		return self.postTitle

def getContentFromCleanURL(url, postType):
    query = db.GqlQuery("SELECT * FROM " + postType + " WHERE cleanURL = '" + url + "'")
    object = query.get()
    if object:
        return object
    else:
        return False

def createCssFromFile():
  cssQuery = db.GqlQuery("SELECT * FROM styleSheet")
  cssCount = cssQuery.count()
  if cssCount < 1:
    mainCSS = styleSheet()
    mainCSS.postTitle = 'main'
    mainCSS.cleanURL = 'main'
    mainCSS.isPublished = True
    cssFile = open('./css/main.css', 'r')
    mainCSS.postText = db.Text(cssFile.read(), encoding="utf-8")
    mainCSS.put()

def createJsFromFile():
  jsQuery = db.GqlQuery("SELECT * FROM jScript")
  jsCount = jsQuery.count()
  if jsCount < 1:
    mainJS = jScript()
    mainJS.postTitle = 'starter'
    mainJS.cleanURL = 'starter'
    mainJS.isPublished = True
    jsFile = open('./js/starter.js', 'r')
    mainJS.postText = db.Text(jsFile.read(), encoding="utf-8")
    mainJS.put()