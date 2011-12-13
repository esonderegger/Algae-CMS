#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

import os
import algaeHtmlBlocks
import algaeModels
import algaePython
pathInfo = os.environ.get('PATH_INFO')
postRequested = pathInfo[7:]
thePost = algaeModels.getContentFromCleanURL(postRequested, 'blogPost')

print '<!DOCTYPE html>'
print '<html lang="en">'
if thePost:
    algaeHtmlBlocks.commonHeader(thePost.postTitle)
else:
    algaeHtmlBlocks.commonHeader('Content Not Found')
print '<body>'
print '<div id="mainDiv">'
algaeHtmlBlocks.titleBlock()
algaeHtmlBlocks.displayNav()
print '<div id="thePost" class="normalContent">'
if thePost:
    thePost.printArticle(link=False)
else:
    print '<h1>Content not found.</h1>'
print '</div>'
print '</div>'
print '</body>'
print '</html>'