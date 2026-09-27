#http://community.wikidot.com/app:whiffle
#Go through all minor planet pages and fix the navigation thing at the bottom
#1. Scrape all of Wikipedia to get a sequential list of named minor planets
#2. Iterate through all pages in the minor planets category
#3. Check if the navigator matches the prevnamed | number | nextnamed format
#4. If not, grab the text, change those numbers, and re-publish pages

import os
import argparse
import sys
import time
import base64
import requests
import json
import re

sys.path.append('..')
from src.wikidotapi import *

def get_wiki_page_nums(span):
	page_nums = []

	if span[0] == 1 or span[0] == 1001:
		#it's totally fucking insane that this fix is necessary. You see this shit?
		page_name = "https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor-planet_names%3A_" + str(span[0]) + "%E2%80%93" + str(span[1]) + "&prop=text&formatversion=2&format=json" # Why, Wikipedia???
	else:
		page_name = "https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor_planet_names%3A_" + str(span[0]) + "%E2%80%93" + str(span[1]) + "&prop=text&formatversion=2&format=json"   
	
	time.sleep(1.0) #Make sure I'm not overloading the system!
	r=requests.get(page_name)
	json_text = json.loads(r.text)
	if 'error' in json_text:
		print("Minor planet page "+str(span[0])+"-"+str(span[1])+" isn't on Wikipedia somehow??")
		return []
	scraped_text = json_text['parse']['text']
	
	scraped_text = remove_text_inside_brackets(scraped_text,"<>")
	scraped_lines = scraped_text.split("\n")
	#now look for the one minor planet 'name'
	for linenum,line in enumerate(scraped_lines):
		if line == "":
			continue
		#find lines that start with a valid number
		firstword = line.partition(" ")[0]
		if not firstword.isdigit():
			continue
		if scraped_lines[linenum-1] == '':
			page_nums.append(firstword)
			
	return page_nums
	

#re.sub("[\(\[].*?[\)\]]", "", x)
def remove_text_inside_brackets(text, brackets="()[]"):
	count = [0] * (len(brackets) // 2) # count open/close brackets
	saved_chars = []
	for character in text:
		for i, b in enumerate(brackets):
			if character == b: # found bracket
				kind, is_close = divmod(i, 2)
				count[kind] += (-1)**is_close # `+1`: open, `-1`: close
				if count[kind] < 0: # unbalanced bracket
					count[kind] = 0  # keep it
				else:  # found bracket to remove
					break
		else: # character is not a [balanced] bracket
			if not any(count): # outside brackets
				saved_chars.append(character)
	return ''.join(saved_chars)



def fix_astropage_sequencing(use_cache):
	print("Fixing astropage navigation sequencing...")
	api = WikidotConnection()
	
	#1.
	all_named_asteroids = []
	
	if use_cache == False:
		iternum=1
		while iternum < 700000:
			all_named_asteroids += get_wiki_page_nums([iternum, iternum+999])
			iternum += 1000
		
		cache = open("numbers_cache.txt", 'w')
		for line in all_named_asteroids:
			cache.write(line + '\n')
	else:
		with open("numbers_cache.txt", 'r') as cache:
			all_named_asteroids = [line.strip() for line in cache]
			
	print("Number of named minor planets: " + str(len(all_named_asteroids)))
	
	#2.
	pagenames = api.server.pages.select({"site": api.Site, "categories": ["minor-planets"]})
	pagenames.remove("minor-planets:1")
	pagenames.remove("minor-planets:69")
	#remove all the minor satellite subpages now:
	pagenames = [page for page in pagenames if page.count(":") == 1]
		
	
	for pagename in pagenames: #do this smarter by parsing get_pages if its slow
		page_dict = api.server.pages.get_one({"site": api.Site, "page": pagename})
		num = page_dict["title"].partition(" ")[0]
		words = page_dict["content"]
		
		#3.
		curr_page = num
		if curr_page not in all_named_asteroids:
			print("Page for " + curr_page + " is not on the Wikipedia named minor planet list.")
			continue
			
		prev_page = all_named_asteroids[all_named_asteroids.index(num)-1]
		next_page = all_named_asteroids[all_named_asteroids.index(num)+1]
		true_navigator = "= [[[minor-planets:"+prev_page+" |< prev]]]   | "+curr_page+" |   [[[minor-planets:"+next_page+" |next >]]]"
		if true_navigator in words:
			continue
		else:
			#4. Find the index of the line with the navigator, then replace it
			print(num)
			#current_navigator = "(= \[\[\[minor\-planets:)[0-9 ]+(\|< prev\]\]\]   \|)[0-9 ]+(\|   \[\[\[minor\-planets:)[0-9 ]+(\|next >\]\]\])"   #FIX THIS!!!!!!!!!!!!!!!
			current_navigator = "= \[\[\[minor\-planets:[0-9a-zA-Z ]+\|< prev\]\]\]   \|[0-9 ]+\|   \[\[\[minor\-planets:[0-9a-zA-Z ]+\|next >\]\]\]"   #FIX THIS!!!!!!!!!!!!!!!
			new_words, numsubs = re.subn(current_navigator,true_navigator,words)
			if numsubs == 0:
				print("Failed to make necessary substitution for " + curr_page)
				continue
				
			try:
				time.sleep(0.1)
				api.server.pages.save_one({"site": api.Site, "page": pagename, "content": new_words})
				api.refresh_pages()
				print("Updated " + curr_page)
			except:
				print("Failed to update page :(") #idk
				sys.exit()
				
if __name__ == "__main__":
	fix_astropage_sequencing(True)


#https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor_planet_names%3A_4001%E2%80%935000&prop=text&formatversion=2&format=json

