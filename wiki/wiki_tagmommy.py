#http://community.wikidot.com/app:whiffle

import os
import argparse

import time

from whiffle import wikidotapi#, ApiError, SemanticError
api = wikidotapi.connection()

#first, get a list of all minor-planets: pages
pagenames = api.server.pages.select({"site": api.Site, "categories": ["minor-planets"]})

#iterate through all minor planets
#give it needs-image tag if it has no #.png
#remove that tag if it does have it
for pagename in pagenames: #do this smarter by parsing get_pages if its slow
    if True: 
        page_dict = api.server.pages.get_one({"site": api.Site, "page": pagename})
    	taglist = page_dict["tags"]
    	num = page_dict["title"].partition(" ")[0]
    	
        filelist = api.server.files.select({"site": api.Site, "page": pagename})
    	has_image = str(num)+".png" in filelist
    	
    	if has_image:
    	    if "needs-image" in taglist:
                api.remove_tag(pagename, "needs-image", ErrorIfRedundant=True)
                print(num)
        else:
    	    if "needs-image" not in taglist:
                api.add_tag(pagename, "needs-image", ErrorIfRedundant=True)
                print(num)
                
        time.sleep(0.25)


#api.set_page_item("hello", "source", "**Hello World!**", create=True)
