

#no arguments
#goes through all of the images within a directory that fit the format #.png,
#and if they have changed since the last time this was run, updates the wiki with the new image.
#http://community.wikidot.com/app:whiffle

import os
import argparse
import time
import base64
import sys

sys.path.append('..')
from src.wikidotapi import *
import config

api = WikidotConnection()

#create list of images #.png

#iterate; for every image #.png, check if the page exists
#if so, upload the image
#get all # for #.png in folders"
def sync_imagenum_to_pagenum(directory):
	print("Syncing all images in",directory,"to wiki...")
	dirlist = [file[0:-4] for file in os.listdir(directory) if file.endswith(".png")]

	for num in dirlist:
		pagename = "minor-planets:"+str(num)
		if api.page_exists(pagename): 
			fname = str(num) + ".png"
			fileloc = directory + fname
		
			# If theres no wiki image at all, or if local image is newer than wiki image,
			meta_dict = api.server.files.get_meta({"site": api.Site, "page": pagename, "files" : [fname]})
			if meta_dict != []:
				wiki_date = meta_dict[fname]["uploaded_at"][0:10].replace('-','') #e.g. '20180627'
				local_date = time.strftime('%Y%m%d', time.localtime(os.path.getmtime(fileloc)))
				#print(wiki_date, local_date)

			#Then upload the image!
			if local_date > wiki_date or meta_dict == []:
				print(num)
				content_string = ""
				with open(fileloc, "rb") as image_file:
					content_string = base64.b64encode(image_file.read())
		
				api.server.files.save_one({"site": api.Site, "page": pagename, "file": fname, "content": content_string})
				time.sleep(0.1)


#api.set_page_item("hello", "source", "**Hello World!**", create=True)

if __name__ == "__main__":
	sync_imagenum_to_pagenum(config.NSS_location+"handdrawn/")
	sync_imagenum_to_pagenum(config.NSS_location+"autosymbols/")