#!/usr/bin/env python

import feedparser
import urllib
import sys
import sqlite3
import time
import datetime
from lxml.html.clean import Cleaner

"""
*******************************************************************************
 * Copyright © 2010, Mike Roddewig (mike@dietfig.org).
 * All rights reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License v3 as published 
 * by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
*******************************************************************************
"""

### Search Parameters ###

search_terms = ["golden"]
listings = ["apa"]
max_price = 1300
min_price = 2
dog = False
cat = False

### Database Information ###

db_file = "/var/db/craigslist.db"

### Craigslist RSS Search URL ###

rss_generic_link = "http://denver.craigslist.org/search/%s?query=%s&minAsk=%s&maxAsk=%s&bedrooms=2"

# Initialization

db = sqlite3.connect(db_file)
db_cursor = db.cursor()

# Generate the RSS links

rss_links = []
update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for listing in listings:
	for term in search_terms:
		term = urllib.quote(term)
		rss_link = rss_generic_link % (listing, term, min_price, max_price)
		if cat == True:
			rss_link = rss_link + "&addTwo=purrr"
		if dog == True:
			rss_link = rss_link + "&addThree=wooof"
		
		rss_link = rss_link + "&format=rss"

		rss_links.append(rss_link)
		
# Retrieve the RSS feeds

cleaner = Cleaner(remove_unknown_tags=False, allow_tags=['img', 'p', 'a', 'b', 'em', 'div']);

for rss_link in rss_links:
	listings = feedparser.parse(rss_link)
	
	for listing in listings.entries:
		title = listing["title"]
		url = listing["link"]
		text = cleaner.clean_html(listing["description"])
		
		db_cursor.execute("""SELECT last_update FROM listings WHERE title = ?""", (title,))
		
		if db_cursor.fetchone() == None:
			db_cursor.execute("""
				INSERT INTO listings 
				(url, title, text, last_update, new, found) 
				VALUES (?, ?, ?, ?, ?, ?)""",
				(url, title, text, update_time, 1, update_time,)
			)
		else:
			db_cursor.execute("""
				UPDATE listings
				SET last_update = ?
				WHERE title = ?
				""",
				(update_time, title,)
			)

# Clean out expired entries

db_cursor.execute("""
	DELETE FROM listings
	WHERE last_update != ?
	""",
	(update_time,)
)

db.commit()
db.close()
