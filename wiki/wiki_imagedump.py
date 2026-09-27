#main function takes in wiki page and directory
#syncs/dumps all images in that directory to page
#when i autorun this script, it will sync all of my big pages for me
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


def dump_imagesdir_to_wikipage(directory, pagename):
	print("Dumping images from "+ directory + " to http://nightskysymbology.wikidot.com/" + pagename + " ...")

	if os.path.isdir(directory) != True:
		print("Directory doesn't exist!")
		return
	else:
		dirlist = [file for file in os.listdir(directory) if file.endswith(".png")]


	for fname in dirlist:
		if api.page_exists(pagename): 
			fileloc = directory + fname
		
			# If theres no wiki image at all, or if local image is newer than wiki image,
			meta_dict = api.server.files.get_meta({"site": api.Site, "page": pagename, "files" : [fname]})
			local_date = 0
			wiki_date = 0
			if meta_dict != []:
				wiki_date = meta_dict[fname]["uploaded_at"][0:10].replace('-','') #e.g. '20180627'
				local_date = time.strftime('%Y%m%d', time.localtime(os.path.getmtime(fileloc)))
				#print(wiki_date, local_date)

			#Then upload the image!
			if local_date > wiki_date or meta_dict == []:
				print("... " + fname)
				content_string = ""
				with open(fileloc, "rb") as image_file:
					content_string = base64.b64encode(image_file.read())
		
				api.server.files.save_one({"site": api.Site, "page": pagename, "file": fname, "content": content_string})
				time.sleep(0.1)
		else:
			print("Page doesn't exist!")
			return


if __name__ == "__main__":
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/jovian/","planets:jupiter")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/saturnian/","planets:saturn")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/uranian/","planets:uranus")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/neptunian/","planets:neptune")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/exoplanets/","exoplanets")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/other/fictional/","fictional")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/other/proposals/","proposed")
	dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/other/osiris-rex-proposals/","101955contest")

