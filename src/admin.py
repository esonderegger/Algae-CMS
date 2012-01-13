#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

from google.appengine.ext import db
import cgi
import os
import Cookie
import algaeHtmlBlocks
import algaeModels
import algaePython
import algaeUserConfig
	
def printBody():
	print "<body>"
	printMainDiv()
	print "</body>"
	
def loggedIn():
	thiscookie = Cookie.SimpleCookie()
	cookie_string = os.environ.get('HTTP_COOKIE')
	if cookie_string:
		thiscookie.load(cookie_string)
		if thiscookie.has_key('username') and thiscookie.has_key('session'):
		  if algaePython.verifiedSession(thiscookie['username'].value, thiscookie['session'].value):
			  return True
	return False

def printMainDiv():
	algaeHtmlBlocks.titleBlock("Admin Page")
	if loggedIn():
		printAdminPage()
	else:
		printLoginForm()

def printLoginForm():
	print "<div id='loginForm'>"
	badInfo = form.getfirst("bad", "")
	if badInfo == 'user':
		print '<p>incorrect username. please try again.</p>'
	elif badInfo == 'password':
		print '<p>incorrect password. please try again.</p>'
	print "<form action='login' method='POST'>"
	print '<p class="textDescriptor">username: </p><input type="text" name="userName" class="adminString" />'
	print '<p class="textDescriptor">password: </p><input type="password" name="password" class="adminString" />'
	print "<div class='theButtons'><input type='submit' value='Log In' class='submitButton' /></div>"
	print "</form>"
	print "</div>"

def printAdminPage():
	whatToEdit = form.getfirst("edit", "newpost")
	adminNav()
	editorSection(whatToEdit)

def editorSection(val):
	if val == 'basicPage':
		pagesSection()
	elif val == 'image':
		imagesSection()
	elif val == 'navLink':
		navSection()
	elif val == 'siteUser':
		usersSection()
	elif val == 'styleSheet':
		cssSection()
	elif val == 'jScript':
		jsSection()
	else:
		print '<div id="adminContent">'
		editID = form.getfirst("key", "")
		if editID == "":
			newPostForm()
		else:
			existingPostForm(editID)
		allLinksOfType('blogPost')
		print '</div>'

def newPostForm():
	print "<div id='postForm' class='adminEditor'>"
	print "<form action='editContent' method='POST'>"
	print "<input type='hidden' name='contentType' value='blogPost' />"
	print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" />'
	print '<p class="textDescriptor">Link (optional): </p><input type="text" name="linkURL" class="adminString" />'
	print '<textarea name="postText" class="adminText"></textarea>'
	print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished"/>'
	print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/></div>"
	print "</form>"
	print "</div>"

def existingPostForm(ID):
	post = algaeModels.blogPost.get(ID)
	print "<div id='postForm' class='adminEditor'>"
	print "<form action='editContent' method='POST'>"
	saved = form.getfirst("saved", "no")
	if saved == "yes" and post.isPublished:
		print '<p class="editorAlert">Post saved. <a href="/posts/' + post.cleanURL + '">view</a></p>'
	elif saved == "yes":
		print '<p class="editorAlert">Post saved.</p>'
	print "<input type='hidden' name='contentType' value='blogPost' />"
	print "<input type='hidden' name='postID' value='" + ID +"' />"
	print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" value="' + cgi.escape(post.postTitle.encode('utf-8'), True) + '" />'
	print '<p class="textDescriptor">Link (optional): </p><input type="text" name="linkURL" class="adminString" value="' + post.linkUrl().encode('utf-8') + '" />'
	print '<textarea name="postText" class="adminText">' + cgi.escape(post.postText.encode('utf-8'), True) + '</textarea>'
	if post.isPublished:
		print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished" checked/>'
	else:
		print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished"/>'
	print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/>"
	print '<a href="/editContent?contentType=delete&amp;cType=blogPost&amp;postID=' + ID + '" class="deleteButton">Delete</a></div>'
	print "</form>"
	print "</div>"

def pagesSection():
	print '<div id="adminContent">'
	editID = form.getfirst("key", "")
	if editID == "":
		newPageForm()
	else:
		existingPageForm(editID)
	allLinksOfType('basicPage')
	print '</div>'

def newPageForm():
	print "<div id='pageForm' class='adminEditor'>"
	print "<form action='editContent' method='POST'>"
	print "<input type='hidden' name='contentType' value='basicPage' />"
	print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" />'
	print '<textarea name="postText" class="adminText"></textarea>'
	print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished"/>'
	print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/></div>"
	print "</form>"
	print "</div>"

def existingPageForm(ID):
	post = algaeModels.basicPage.get(ID)
	print "<div id='pageForm' class='adminEditor'>"
	print "<form action='editContent' method='POST'>"
	saved = form.getfirst("saved", "no")
	if saved == "yes" and post.isPublished:
		print '<p class="editorAlert">Page saved. <a href="/pages/' + post.cleanURL + '">view</a></p>'
	elif saved == "yes":
		print '<p class="editorAlert">Page saved.</p>'
	print "<input type='hidden' name='contentType' value='basicPage' />"
	print "<input type='hidden' name='postID' value='" + ID +"' />"
	print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" value="' + cgi.escape(post.postTitle.encode('utf-8'), True) + '" />'
	print '<textarea name="postText" class="adminText">' + cgi.escape(post.postText.encode('utf-8'), True) + '</textarea>'
	if post.isPublished:
		print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished" checked/>'
	else:
		print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished"/>'
	print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/>"
	print '<a href="/editContent?contentType=delete&amp;cType=basicPage&amp;postID=' + ID + '" class="deleteButton">Delete</a></div>'
	print "</form>"
	print "</div>"

def allLinksOfType(contentType, orderBy='postTime DESC'):
	print "<div id='editorLinks' class='adminLinks'>"
	keysAndTitles = algaePython.keysAndTitles(contentType, orderBy)
	for keyAndTitle in keysAndTitles:
		print '<p><a href="admin?edit=' + contentType + '&amp;key=' + str(keyAndTitle[0]) + '">' + cgi.escape(keyAndTitle[1]) + '</a></p>'
	print "</div>"

def imagesSection():
  print "<div id='adminContent'>"
  editID = form.getfirst("key", "")
  if editID == "":
    newImageForm()
  else:
    existingImageForm(editID)
  imagesLinks()
  print "</div>"

def imagesLinks():
  print "<div id='editorLinks' class='adminLinks'>"
  keysAndTitles = algaePython.keysAndTitles('algaeImage', 'postTime DESC')
  for keyAndTitle in keysAndTitles:
    theImage = algaeModels.algaeImage.get(keyAndTitle[0])
    print '<div class="imageEditThumb">'
    print '<a href="admin?edit=image&amp;key=' + str(keyAndTitle[0]) + '"><img src="/images/' + theImage.cleanURL + '_sm' + theImage.fileExt() + '" alt="' + theImage.postTitle + '" /></a>'
    print "</div>"
  print "</div>"

def newImageForm():
	print "<div id='userForm' class='adminEditor'>"
	print '<form action="editContent" enctype="multipart/form-data" method="post">'
	print "<input type='hidden' name='contentType' value='image' />"
	print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" />'
	print '<div><p class="textDescriptor">Image: </p><input type="file" name="img"/></div>'
	print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished" checked/>'
	print '<div class="theButtons"><input type="submit" value="Upload" class="submitButton"/></div>'
	print '</form>'
	print '</div>'
	
def existingImageForm(ID):
  theImage = algaeModels.algaeImage.get(ID)
  print "<div id='userForm' class='adminEditor'>"
  print '<div class="imageEditLinks">'
  print '<img src="/images/' + theImage.cleanURL + '_md' + theImage.fileExt() + '" alt="' + theImage.postTitle + '"/>'
  print '<p>Links:</p>'
  print '<p><a href="/images/'+ theImage.cleanURL + '_sm' + theImage.fileExt() + '">Small</a></p>'
  print '<p><a href="/images/'+ theImage.cleanURL + '_md' + theImage.fileExt() + '">Medium</a></p>'
  print '<p><a href="/images/'+ theImage.cleanURL + '_lg' + theImage.fileExt() + '">Large</a></p>'
  print '<p><a href="/images/'+ theImage.cleanURL + theImage.fileExt() + '">Original</a></p>'
  print '</div>'
  print '<form action="editContent"enctype="multipart/form-data" method="post">'
  print '<div class="imageEditForm">'
  print "<input type='hidden' name='contentType' value='image' />"
  print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" value="' + cgi.escape(theImage.postTitle.encode('utf-8'), True) + '" />'
  print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished" checked/>'
  print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/>"
  print '<a href="/editContent?contentType=delete&amp;cType=image&amp;postID=' + ID + '" class="deleteButton">Delete</a></div>'
  print '</div>'
  print '</form>'
  print '</div>'


def navSection():
  editID = form.getfirst("key", "")
  navQuery = db.GqlQuery("SELECT * FROM navLink ORDER BY rank ASC")
  navs = navQuery.fetch(1000)
  print "<div id='navForm' class='adminNoLinks'>"
  for nav in navs:
  	if editID == str(nav.key()):
  		navForm(editID)
  	else:
	  	print '<div class="navAdminGroup">'
	  	print '<p class="linkDescriptor">Title (required): </p>' + nav.postTitle.encode('utf-8') + '<br />'
	  	print '<p class="linkDescriptor">Link (required): </p><a href="' + nav.theLink.encode('utf-8') + '">' + nav.theLink.encode('utf-8') + '</a>'
	  	if nav.altText != '':
	  		print '<br /><p class="linkDescriptor">Alt Text (optional): </p>' + nav.altText.encode('utf-8')
	  	print '<div class="navAdminOptions">'
	  	print '<a href="admin?edit=navLink&amp;key=' + str(nav.key()) + '">Edit</a>'
	  	if nav.rank > 0:
	  		print '<a href="editContent?contentType=navOrder&direction=up&key=' + str(nav.key()) + '">Move Up</a>'
	  	if nav.rank + 1 < navQuery.count():
	  		print '<a href="editContent?contentType=navOrder&direction=down&key=' + str(nav.key()) + '">Move Down</a>'
	  	print '</div>'
	  	print '</div>'
  if editID == "":
  	navForm("")
  print "</div>"

def navForm(ID = ""):
  print "<form action='editContent' method='POST'>"
  print "<input type='hidden' name='contentType' value='navLink' />"
  if ID != "":
    print "<input type='hidden' name='postID' value='" + ID +"' />"
    nav = algaeModels.navLink.get(ID)
    print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" value="' + cgi.escape(nav.postTitle.encode('utf-8'), True) + '" />'
    print '<p class="textDescriptor">Link (required): </p><input type="text" name="theLink" class="adminString" value="' + cgi.escape(nav.theLink.encode('utf-8'), True) + '" />'
    print '<p class="textDescriptor">Alt Text (optional): </p><input type="text" name="altText" class="adminString" value="' + cgi.escape(nav.altText.encode('utf-8'), True) + '" />'
    print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/>"
    print '<a href="/editContent?contentType=delete&amp;cType=navLink&amp;postID=' + ID + '" class="deleteButton">Delete</a></div>'
  else:
    print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" />'
    print '<p class="textDescriptor">Link (required): </p><input type="text" name="theLink" class="adminString" />'
    print '<p class="textDescriptor">Alt Text (optional): </p><input type="text" name="altText" class="adminString" />'
    print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/></div>"
  print "</form>"

def usersSection():
	print '<div id="adminContent">'
	print "<div id='userForm' class='adminEditor'>"
	editID = form.getfirst("key", "")
	if editID == "":
		userForm()
	else:
		userForm(editID)
	print '</div>'
	allLinksOfType('siteUser', 'userName ASC')
	print '</div>'

def userForm(ID = ""):
	print "<form action='editContent' method='POST'>"
	print "<input type='hidden' name='contentType' value='siteUser' />"
	if ID != "":
		print "<input type='hidden' name='postID' value='" + ID +"' />"
		user = algaeModels.siteUser.get(ID)
		print '<p class="textDescriptor">Username: </p><input type="text" name="userName" class="adminString" value="' + cgi.escape(user.userName.encode('utf-8'), True) + '" />'
		print '<p class="textDescriptor">Display Name: </p><input type="text" name="displayName" class="adminString" value="' + cgi.escape(user.displayName.encode('utf-8'), True) + '" />'
		print '<p class="textDescriptor">Email: </p><input type="email" name="userEmail" class="adminString" value="' + cgi.escape(user.userEmail.encode('utf-8'), True) + '" />'
		print '<p class="textDescriptor">Password: </p><input type="password" name="pWord" class="adminString" />'
		print '<p class="textDescriptor">Role: </p><select name="role" class="adminSelect">'
		print '<option value="admin">Admin</option>'
		print '<option value="author">Author</option>'
		print '<option value="designer">Designer</option>'
		print '</select>'
	else:
		print '<p class="textDescriptor">Username: </p><input type="text" name="userName" class="adminString" />'
		print '<p class="textDescriptor">Display Name: </p><input type="text" name="displayName" class="adminString" />'
		print '<p class="textDescriptor">Email: </p><input type="email" name="userEmail" class="adminString" />'
		print '<p class="textDescriptor">Password: </p><input type="password" name="pWord" class="adminString" />'
		print '<p class="textDescriptor">Role: </p><select name="role" class="adminSelect">'
		print '<option value="admin">Admin</option>'
		print '<option value="author">Author</option>'
		print '<option value="designer">Designer</option>'
		print '</select>'
	print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/></div>"
	print "</form>"

def cssSection():
	print '<div id="adminContent">'
	editID = form.getfirst("key", "")
	if editID == "":
		newDesignForm('styleSheet')
	else:
		existingDesignForm(editID, 'styleSheet')
	allLinksOfType('styleSheet')
	print '</div>'

def jsSection():
	print '<div id="adminContent">'
	editID = form.getfirst("key", "")
	if editID == "":
		newDesignForm('jScript')
	else:
		existingDesignForm(editID, 'jScript')
	allLinksOfType('jScript')
	print '</div>'

def newDesignForm(cType):
  if cType == 'styleSheet':
    algaeModels.createCssFromFile()
  else:
    algaeModels.createJsFromFile()
  print "<div id='" + cType + "Form' class='adminEditor'>"
  print "<form action='editContent' method='POST'>"
  print "<input type='hidden' name='contentType' value='" + cType + "' />"
  print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" />'
  print '<textarea name="postText" class="adminText"></textarea>'
  print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished"/>'
  print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/></div>"
  print "</form>"
  print "</div>"

def existingDesignForm(ID, cType):
	if cType == 'styleSheet':
		post = algaeModels.styleSheet.get(ID)
	else:
		post = algaeModels.jScript.get(ID)
	print "<div id='" + cType + "Form' class='adminEditor'>"
	print "<form action='editContent' method='POST'>"
	saved = form.getfirst("saved", "no")
	if saved == "yes" and post.isPublished:
		if cType == 'styleSheet':
			print '<p class="editorAlert">Style Sheet saved. <a href="/css/' + post.cleanURL + '">view</a></p>'
		else:
			print '<p class="editorAlert">Javascript saved. <a href="/js/' + post.cleanURL + '">view</a></p>'
	elif saved == "yes":
		print '<p class="editorAlert">Page saved.</p>'
	print "<input type='hidden' name='contentType' value='" + cType + "' />"
	print "<input type='hidden' name='postID' value='" + ID +"' />"
	print '<p class="textDescriptor">Title (required): </p><input type="text" name="postTitle" class="adminString" value="' + cgi.escape(post.postTitle.encode('utf-8'), True) + '" />'
	print '<textarea name="postText" class="adminText">' + cgi.escape(post.postText.encode('utf-8'), True) + '</textarea>'
	if post.isPublished:
		print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished" checked/>'
	else:
		print '<p class="textDescriptor">Published: </p><input type="checkbox" name="isPublished"/>'
	print "<div class='theButtons'><input type='submit' value='Save' class='submitButton'/>"
	print '<a href="/editContent?contentType=delete&amp;cType=' + cType + '&amp;postID=' + ID + '" class="deleteButton">Delete</a></div>'
	print "</form>"
	print "</div>"

def adminNav():
	print '<nav>'
	print '<ul>'
	print '<li><a href="admin?edit=blogPost">Posts</a></li>'
	print '<li><a href="admin?edit=basicPage">Pages</a></li>'
	print '<li><a href="admin?edit=image">Images</a></li>'
	print '<li><a href="admin?edit=navLink">Navigation</a></li>'
	print '<li><a href="admin?edit=siteUser">Users</a></li>'
	print '<li><a href="admin?edit=styleSheet">CSS</a></li>'
	print '<li><a href="admin?edit=jScript">Javascript</a></li>'
	print '<li><a href="logout">Log Out</a></li>'
	print '</ul>'
	print '</nav>'

form = cgi.FieldStorage()

print 'Content-Type: text/html\n'
print '<!DOCTYPE html>'
print '<html lang="en">'
algaeHtmlBlocks.commonHeader(algaeUserConfig.siteTitle.encode('utf-8') + " Admin Page")
printBody()
print '</html>'