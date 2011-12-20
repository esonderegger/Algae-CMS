#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

import os
import algaeModels

pathInfo = os.environ.get('PATH_INFO')
postRequested = pathInfo[8:]
if postRequested.find('_') > 0:
  imageRequested = postRequested[:postRequested.find('_')]
  versionRequested = postRequested[postRequested.find('_') + 1:postRequested.find('_') + 3]
elif postRequested.find('.') > 0:
  imageRequested = postRequested[:postRequested.find('.')]
  versionRequested = 'original'
else:
  imageRequested = postRequested
  versionRequested = 'original'
theImage = algaeModels.getContentFromCleanURL(imageRequested, 'algaeImage')

if theImage:
  print 'Content-Type: ' + theImage.mimeType + '\n'
  if versionRequested == 'sm':
    print theImage.smData
  elif versionRequested == 'md':
    print theImage.mdData
  else:
    print theImage.imgData
else:
  print '<!DOCTYPE html>'
  print '<html lang="en">'
  print '<h1>Content not found.</h1>'
  print '</html>'