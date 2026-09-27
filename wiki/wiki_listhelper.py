
#argument: people_list.txt, places_list.txt, etc.
#goes through a wikipedia source and helps you make a page for all entries
#http://community.wikidot.com/app:whiffle

import os
import argparse

from whiffle import wikidotapi, ApiError, SemanticError




api = wikidotapi.connection(identity)

#create list of minor planets, with categories attached

#iterate; for each number without a corresponding page,
#print the row contents, and ask for referent description and symbol description
#check if theres a #.png alread; if so, upload items
#user prompt add tags. Automatically add needs-image if the earlier step found no image
for mp in mp_list:


#api.set_page_item("hello", "source", "**Hello World!**", create=True)