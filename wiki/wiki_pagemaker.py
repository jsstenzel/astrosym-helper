#Guide the user to fill in pages for images in handdrawn/ that dont yet have pages
#http://community.wikidot.com/app:whiffle

import os
import argparse
import sys

from whiffle import wikidotapi#, ApiError, SemanticError
import time
import base64

import requests
import json
import random
import subprocess


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


def get_wiki_scrape_meaning(name):
    num = int(name.partition(" ")[0])

    iternum = 1
    span = []
    while iternum < 1000000:
        if iternum <= num and iternum+999 >= num:
            span = [iternum,iternum+999]
            break
        iternum +=1000
    if span == []:
        sys.exit("Number doesn't fucking exist you kumquat")
    
    if span[0] == 1 or span[0] == 1001:
        #it's totally fucking insane that this fix is necessary. You see this shit?
        page_name = "https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor-planet_names%3A_" + str(span[0]) + "%E2%80%93" + str(span[1]) + "&prop=text&formatversion=2&format=json" # Why, Wikipedia???
    else:
        page_name = "https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor_planet_names%3A_" + str(span[0]) + "%E2%80%93" + str(span[1]) + "&prop=text&formatversion=2&format=json"   
    
    r=requests.get(page_name)
    json_text = json.loads(r.text)
    if 'error' in json_text:
        sys.exit("Minor planet page "+str(span[0])+"-"+str(span[1])+" isn't on Wikipedia somehow??")
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
        if name in line:
            #print(line)
            #print(scraped_lines[linenum+2])
            return scraped_lines[linenum+2]
    
    #if you got here, the page search failed
    print(span)
    sys.exit("Minor planet meaning for "+name+" isn't on Wikipedia")
        

def page_text(number):
    prev = number-1
    post = number+1
    referent = raw_input("Description for asteroid symbol referent " + str(number) +":")
    symbol = raw_input("Description of asteroid symbol:")
    pagetext = '''[[table style="width: 100%;"]]\n[[row]]\n[[cell style="width: 100%; font-size: 110%; border: 1px solid grey; background-color: #000000; color:grey; padding: 10px;"]]\n\n[[f>image ''' + str(number) + '''.png size="thumbnail"]]\n\n''' + str(referent) + '''\n\n''' + str(symbol) + '''\n\n= [[[minor-planets:''' + str(prev) + ''' |< prev]]]   | ''' + str(number) + ''' |   [[[minor-planets:''' + str(post) + ''' |next >]]]\n------\n\n\n[[/cell]]\n[[/row]]\n[[/table]]\n\n+ Comments\n[[module Comments]]'''
    return pagetext



api = wikidotapi.connection()

#create list of images

#iterate; for every image #.png, create a page minor-planets:# if that page does not exist
#then, query the user for page name, i.e. 11 Parthenope
#then, query user for description, and add full text.
#then, let the user give tags over and over, prompting some common ones (nationality, gender, letters, elements, person) until they give the keyword 'done'
handdrawn_list = [f[0:-4] for f in os.listdir("./handdrawn/") if f.endswith(".png") and f[0:-4].isdigit()]
#handdrawn_list = sorted([int(file) for file in handdrawn_list if file.isdigit()])
random.shuffle(handdrawn_list)

for directory,dirlist in [["handdrawn/",handdrawn_list]]:
    for num in dirlist:
        pagename = "minor-planets:"+str(num)
        if not api.page_exists(pagename):
            fname = str(num) + ".png"
            fileloc = directory + fname
            
            #infodump
            r=requests.get("https://ssd-api.jpl.nasa.gov/sbdb.api?des=" + str(num) + "&discovery=true&no-orbit=1")
            json_text = json.loads(r.text)
            if not 'object' in json_text:
                sys.exit("Something weird happened, JPL SSD can't find "+str(num))
            shortname = json_text['object']['shortname']
            print(shortname)
            #if 'citation' in json_text['discovery']:
            #    citation = json_text['discovery']['citation']
            #else:
            #    citation = "ERROR: No citation"
            #print(citation)
            print(get_wiki_scrape_meaning(shortname))
            p = subprocess.Popen(['xdg-open', directory+fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            title = shortname
            text = page_text(int(num))
            api.server.pages.save_one({"site": api.Site, "page": pagename, "title": title, "content": text, "save_mode": "create"})
            api.refresh_pages()
            
            taglist = [str(item) for item in raw_input("Enter the spaced list of tags, ending with ENTER : ").split()]
            for tag in taglist:
                print(pagename)
                print(tag)
                api.add_tag(pagename, tag, ErrorIfRedundant=False)
                time.sleep(0.1)


            #upload image
            content_string = ""
            with open(fileloc, "rb") as image_file:
                content_string = base64.b64encode(image_file.read())
    	
            api.server.files.save_one({"site": api.Site, "page": pagename, "file": fname, "content": content_string})
            
            #done
            p.kill()
