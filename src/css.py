#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

import os
import algaeModels
pathInfo = os.environ.get('PATH_INFO')
postRequested = pathInfo[5:]
thePage = algaeModels.getContentFromCleanURL(postRequested, 'styleSheet')

if thePage:
  print thePage.postText
elif os.path.exists('./css/' + postRequested):
  file = open('./css/' + postRequested, 'r')
  print file.read()
else:
  print '<!DOCTYPE html>'
  print '<html lang="en">'
  print '<h1>Content not found.</h1>'
  print '</html>'