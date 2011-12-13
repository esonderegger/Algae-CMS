# Algae-CMS
## A Little Google App Engine CMS, written in Python

Algae-CMS is a minimalist content management system, written in Python, and designed
to be hosted on Google's App Engine. Posts and pages are written in 
[Markdown](http://daringfireball.net/projects/markdown/) and content, CSS, and Javascript are
all editable via the browser. Algae-CMS aims to generate elegant, valid HTML5 source code.

## Why Google App Engine?
App Engine offers scalability and pricing that are hard to find elsewhere. Setting up a content
management system that can scale past one server instance on Amazon's EC2 platform requires
considerable expertise. Also, many users of Algae-CMS will likely fit into Google's free tier
for the service.

## Why Markdown?
On [John Gruber's page for Markdown](http://daringfireball.net/projects/markdown/), he describes 
better than I could:

>Markdown is a text-to-HTML conversion tool for web writers. Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML).

For the purpose of this CMS, Markdown allows for rapid content creation without resorting to tools
like [CKEditor](http://ckeditor.com/). This allows the author to have full control of their
source code without having to always type commonly used tags.

## Special Thanks
Algae-CMS depends on two python packages, without which the project would not be possible.

[markdown2](https://github.com/trentm/python-markdown2), by Trent Mick.

[gae-pytz](http://code.google.com/p/gae-pytz/), allows for parsing the datetime info in the
App Engine datastore in a local timezone the site.