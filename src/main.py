#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import cgi
import myHtmlBlocks
import algaePython
import algaeUserConfig

def printBody():
	#print '<body onload="getPosts(2)">'
	print '<body>'
	printMainDiv()
	print '</body>'

def printMainDiv():
	myHtmlBlocks.titleBlock()
	myHtmlBlocks.displayNav()
	print '<div id="thePosts" class="normalContent">'
	form = cgi.FieldStorage()
	pageNum = int(form.getfirst("page", 0))
	myHtmlBlocks.getPostsContent(algaeUserConfig.postsPerPage, pageNum*algaeUserConfig.postsPerPage)
	print "</div>"
	postsCount = algaePython.getPostsCount()
	if postsCount > 2 or pageNum > 0:
		print "<div id='prevNextPage'>"
		if pageNum > 1:
			print '<div id="prevPage"><a href="/?page=' + str(pageNum - 1) + '">Previous Page</a></div>'
		elif pageNum == 1:
			print '<div id="prevPage"><a href="/">Previous Page</a></div>'
		if postsCount > algaeUserConfig.postsPerPage*pageNum + algaeUserConfig.postsPerPage:
			print '<div id="nextPage"><a href="/?page=' + str(pageNum + 1) + '">Next Page</a></div>'
		print "</div>"

print '<!DOCTYPE html>'
print '<html lang="en">'
myHtmlBlocks.commonHeader()
printBody()
print '</html>'