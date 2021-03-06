#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

import os
import algaeModels
pathInfo = os.environ.get('PATH_INFO')
postRequested = pathInfo[4:]
thePage = algaeModels.getContentFromCleanURL(postRequested, 'jScript')

if thePage:
  print 'Content-Type: text/x-js \n'
  print thePage.postText
elif os.path.exists('./js/' + postRequested):
  file = open('./js/' + postRequested, 'r')
  print 'Content-Type: text/x-js \n'
  print file.read()
else:
  print '<!DOCTYPE html>'
  print '<html lang="en">'
  print '<h1>Content not found.</h1>'
  print '</html>'