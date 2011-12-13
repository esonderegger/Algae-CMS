#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import hashlib
import algaeUserConfig
import algaeModels

def verifiedUser(username):
	userQuery = db.GqlQuery("SELECT * FROM siteUser WHERE userName = '" + username + "'")
	user = userQuery.get()
	if user:
		return True
	elif username == algaeUserConfig.rootUserName:
		# this is to initialize a user in the datastore for the root user.
		rootUser = algaeModels.siteUser()
		rootUser.userName = algaeUserConfig.rootUserName
		rootUser.displayName = algaeUserConfig.rootDisplayName
		rootUser.saltedPwd = hashlib.md5(algaeUserConfig.rootPassword + algaeUserConfig.passSalt).hexdigest()
		rootUser.userEmail = algaeUserConfig.rootEmail
		rootUser.role = 'admin'
		rootUser.put()
		return True
	return False

def verifiedPassword(username, password):
	userQuery = db.GqlQuery("SELECT * FROM siteUser WHERE userName = '" + username + "'")
	user = userQuery.get()
	if user:
		if user.saltedPwd == hashlib.md5(password + algaeUserConfig.passSalt).hexdigest():
			return True
	return False
	
def verifiedSession(username, sessionID):
	sessionQuery = db.GqlQuery("SELECT * FROM userSession WHERE sessionID = '" + sessionID + "'")
	session = sessionQuery.get()
	if session:
		if username == session.sessionUserName:
			return True
	return False

# def getUser(username):
# 	userQuery = db.GqlQuery("SELECT * FROM siteUser WHERE userName = '" + username + "'")
# 	user = userQuery.get()
# 	if user:
# 		return user
# 	return False

def getPostsContent(num, offset):
	postsQuery = db.GqlQuery("SELECT * FROM blogPost WHERE isPublished = True ORDER BY postTime DESC")
	posts = postsQuery.fetch(num, offset)
	if len(posts) > 0:
		for post in posts:
			post.printArticle(link=True)
	else:
		print '<article>'
		print "<h2>Welcome!</h2>"
		print "<p>It looks like this is a new site.</p>"
		print "<p>Click over to the <a href='admin'>admin page</a> to add some content.</p>"
		print '</article>'

def getPostsCount():
	# fails if over 1000 published posts. A sharded counter would be better
	postsQuery = db.GqlQuery("SELECT * FROM blogPost WHERE isPublished = True")
	postsCount = postsQuery.count()
	return postsCount

def keysAndTitles(postType, orderBy='postTime DESC'):
	theList = []
	postsQuery = db.GqlQuery("SELECT * FROM " + postType + " ORDER BY " + orderBy)
	posts = postsQuery.fetch(1000)
	for post in posts:
		theList.append([post.key(), str(post)])
	return theList

def noDupeURL(url, postType):
	testURL = url
	query = db.GqlQuery("SELECT * FROM " + postType + " WHERE cleanURL = '" + url + "'")
	counter = 2
	while query.get():
		testURL = url + '-' + str(counter)
		query = db.GqlQuery("SELECT * FROM " + postType + " WHERE cleanURL = '" + testURL + "'")
		counter += 1
	return testURL
