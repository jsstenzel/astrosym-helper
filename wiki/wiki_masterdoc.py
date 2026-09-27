

#no arguments
#goes through the masterdoc excel and helps you make a page for all entries
#http://community.wikidot.com/app:whiffle

import os
import argparse

from whiffle import wikidotapi, ApiError, SemanticError




api = wikidotapi.connection(identity)

#create list of nonempty rows in master doc

#iterate; for each number without a corresponding page,
#print the cell contents, and ask for referent description and symbol description
#check if theres a #.png; if so, upload items
#user prompt add tags. Automatically add needs-image if the earlier step found no image
#if so, upload the image
for image in image_list:


#api.set_page_item("hello", "source", "**Hello World!**", create=True)