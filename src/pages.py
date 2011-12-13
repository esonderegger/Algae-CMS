#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

import os
import algaeHtmlBlocks
import algaeModels
import algaePython
pathInfo = os.environ.get('PATH_INFO')
postRequested = pathInfo[7:]
thePage = algaeModels.getContentFromCleanURL(postRequested, 'basicPage')

print '<!DOCTYPE html>'
print '<html lang="en">'
if thePage:
  algaeHtmlBlocks.commonHeader(thePage.postTitle.encode('utf-8'))
else:
  algaeHtmlBlocks.commonHeader('Content Not Found')
print '<body>'
algaeHtmlBlocks.titleBlock()
algaeHtmlBlocks.displayNav()
print '<div id="thePost" class="normalContent">'
if thePage:
  print thePage.markdownText.encode('utf-8')
else:
  print '<h1>Content not found.</h1>'
print '</div>'
print '</body>'
print '</html>'