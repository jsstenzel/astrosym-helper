

#no arguments

#script for setting all minor planet image code to this format:
#[[f>image minor-planets:20/20.png size="thumbnail"]]
#http://community.wikidot.com/app:whiffle

import os
import argparse
import time
import sys

sys.path.append('..')
from src.wikidotapi import *
import config

def fix_image_formats():
	print("Iterating through all asteroid pages to fix image formatting...", flush=True)
	api = WikidotConnection()

	#These commands work:
	'''
	print(api.server.files.select({"site": api.Site, "page": "minor-planets:4"}))
	page_dict = api.server.pages.get_one({"site": api.Site, "page": "minor-planets:4"})
	print(page_dict['content'])
	'''

	#iterate through every page minor-planets:# if that page exists
	#then, use regex to find the image line
	#then, replace it with [[f>image minor-planets:#/#.png size="thumbnail"]]

	for num in range(1,500000):   #do this smarter by parsing get_pages if its slow
		pagename = "minor-planets:" + str(num)
		if api.page_exists(pagename): 
			print(num, flush=True)
			page_dict = api.server.pages.get_one({"site": api.Site, "page": pagename})
			page_text = page_dict['content']
			old_line = '[[f>image :first size="thumbnail"]]'
			new_line = '[[f>image ' + str(num) + '.png size="thumbnail"]]'
			page_text = page_text.replace(old_line, new_line)
			print(page_text, flush=True)
			api.set_page_item(pagename, 'content', page_text, create=False)
			
			time.sleep(0.5)

		
#print(api.get_pages())
#api.set_page_item("hello", "source", "**Hello World!**", create=True)