#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import algaeModels
import algaeUserConfig

def commonHeader(title=""):
	print '<head>'
	print '<meta charset="utf-8" />'
	if title == "":
		title = algaeUserConfig.siteTitle
	print '<title>' + title + '</title>'
	print '<link href="/stylesheets/main.css" rel="stylesheet" />'
	print '<link href="http://fonts.googleapis.com/css?family=Convergence" rel="stylesheet">'
	print "<link href='http://fonts.googleapis.com/css?family=Inconsolata' rel='stylesheet'>"
	print '<script src="/javascript/starter.js"></script>'
	print '</head>'

def titleBlock(byline=""):
	print '<header id="pageHeader">'
	print '<hgroup>'
	print '<h1><a href="/">' + algaeUserConfig.siteTitle.encode('utf-8') + '</a></h1>'
	if byline == "":
		byline = algaeUserConfig.siteByline.encode('utf-8')
	print "<h2>" + byline + "</h2>"
	print '</hgroup>'
	print "</header>"

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

def displayNav():
  navQuery = db.GqlQuery("SELECT * FROM navLink ORDER BY rank ASC")
  navs = navQuery.fetch(1000)
  if len(navs) > 0:
    print '<nav>'
    print '<ul>'
  for nav in navs:
    if nav.altText == '':
      linkTitle = ''
    else:
      linkTitle = ' title="' + nav.altText.encode('utf-8') + '"'
    print '<li><a href="' + nav.theLink.encode('utf-8') + '"' + linkTitle +'>' + nav.postTitle.encode('utf-8') + '</a></li>'
  if len(navs) > 0:
    print '</nav>'
    print '</ul>'