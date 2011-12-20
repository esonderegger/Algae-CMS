#!/usr/bin/env python
# Copyright (c) 2011 Evan Sonderegger
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

siteTitle = 'New Algae-CMS Site'
siteByline = 'Site Description goes here.'

# Once the admin interface is used for editing users, this info is stored in the datastore and can
# be changed. Deleting the root user in the admin interface resets back to what is saved here.

rootUserName = 'admin'
rootPassword = 'ChangeThis'
rootDisplayName = 'Admin User'
rootEmail = 'admin@youremail.com'

# This is the salt value used to create the hash values that are stored for passwords and
# sessions. It is very important that you change this.

passSalt = 'Mortons'

# This determines how many posts are displayed per page on the main page
postsPerPage = 5

# Set these values for the sizes of scaled down images, in pixels
# it is possible to set x and y independently in editContent.py,
# but the default is to scale x and y the same for simplicity

smallImageSize = 80
mediumImageSize = 240
largeImageSize = 750

# uncomment the timezone you want the server to use.
# if not listed here, look through pytz.common_timezones

siteTimeZone = 'US/Eastern'
# siteTimeZone = 'US/Central'
# siteTimeZone = 'US/Mountain'
# siteTimeZone = 'US/Pacific'
# siteTimeZone = 'US/Pacific'
# siteTimeZone = 'Asia/Tokyo'
# siteTimeZone = 'Asia/Kolkata'
# siteTimeZone = 'Africa/Cairo'
# siteTimeZone = 'Europe/London'