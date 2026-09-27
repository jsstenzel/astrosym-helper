#http://community.wikidot.com/app:whiffle
#Scrape the wikipedia list pages to make my wikidot list pages
#1. take the input range i.e. 12000-14000
#2. iterate through relevant wikipedia pages
#3. Parse that nasty mess into a dict of names and descriptions
#4. convert that dict to a list of formatted table lines
#5. print those lines into an output doc > output.txt

import os
import argparse

from whiffle import wikidotapi#, ApiError, SemanticError
import time
import base64

import requests
import json
import re

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


def page_text(listpage):
    prev = number-1
    post = number+1
    
    referent = '''From the [https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=''' + str(number) + ''' JPL Small-Body DataBase]:\n\n[[table style="width: 75%;margin-right:auto; margin-left:auto;"]]\n[[row]]\n[[cell style="width: 100%; font-size: 100%; border: 1px solid grey; background-color: #F6F9F6; padding: 10px;"]]\n''' + citation +'''\n[[/cell]]\n[[/row]]\n[[/table]]'''
    
    symbol = "The symbol of this minor planet is a " + raw_input("The symbol of this minor planet is a ") + (" over ") + raw_input(" over ")
    
    pagetext = '''[[table style="width: 100%;"]]\n[[row]]\n[[cell style="width: 100%; font-size: 110%; border: 1px solid grey; background-color: #000000; color:grey; padding: 10px;"]]\n\n[[f>image ''' + str(number) + '''.png size="thumbnail"]]\n\n''' + str(referent) + '''\n\n''' + str(symbol) + '''\n\n= [[[minor-planets:''' + str(prev) + ''' |< prev]]]   | ''' + str(number) + ''' |   [[[minor-planets:''' + str(post) + ''' |next >]]]\n------\n\n\n[[/cell]]\n[[/row]]\n[[/table]]\n\n+ Comments\n[[module Comments]]'''
    return pagetext


api = wikidotapi.connection()


def main(listpage, catchwords=[]):
    #grab start and end numbers
    startnum = int(listpage.replace('-',':').split(":")[1])
    endnum = int(listpage.replace('-',':').split(":")[2])
    
    #figure out the list of wikipedia pages you need to check (number of 1000-long subsections)
    #if endnum - startnum > 1000:
    iternum = startnum
    list_spans = []
    while iternum < endnum:
        list_spans.append([iternum,iternum+999])
        iternum +=1000
    #else:
    #    list_spans = [[startnum,endnum]]
    print(list_spans)
    
    content_list = []
    for span in list_spans:
        substart = span[0]
        subend = span[1]
        
        if span[0] == 1 or span[0] == 1001:
            #it's totally fucking insane that this fix is necessary. You see this shit?
            page_name = "https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor-planet_names%3A_" + str(span[0]) + "%E2%80%93" + str(span[1]) + "&prop=text&formatversion=2&format=json" # Why, Wikipedia???
        else:
            page_name = "https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor_planet_names%3A_" + str(span[0]) + "%E2%80%93" + str(span[1]) + "&prop=text&formatversion=2&format=json"   
        
        r=requests.get(page_name)
        json_text = json.loads(r.text)
        if 'error' in json_text:
            continue
        scraped_text = json_text['parse']['text']
        
        
        ##Time to parse into dict of names and meanings
        #remove ugly hypertext
        scraped_text = remove_text_inside_brackets(scraped_text,"<>")
        #split string into list of lines
        scraped_lines = scraped_text.split("\n")
        #assemble dict
        counter = substart
        for linenum,line in enumerate(scraped_lines):
            if line == "":
                continue
            #find lines that start with a valid number
            firstword = line.partition(" ")[0]
            if not firstword.isdigit():
                continue
            if int(firstword) >= counter:
                if scraped_lines[linenum-1] == '' and any(word in scraped_lines[linenum+2] for word in catchwords):
                    print(line)
                    #print(scraped_lines[linenum+2])
                    counter = int(firstword)+1
                    content_list.append([line, scraped_lines[linenum+2]])
                    
    print(len(content_list))
    
    #4. convert that dict to a list of formatted table lines
    preamble = """"[[table style="width: 100%;"]]\n[[row]]\n[[cell style="width: 100%; font-size: 110%; border: 1px solid grey; background-color: #000000;  color:grey; padding: 10px;"]]\n(Names and meanings quoted directly from Wikipedia.)\n"""
    postamble = """\n=  [[[list: |< prev]]] | """ + str(startnum) + """ - """ + str(endnum) + """ |   [[[list: |next >]]]\n------\n\n\n[[/cell]]\n[[/row]]\n[[/table]]"""
    final_table = ""
    for line in content_list:
        name = line[0]
        meaning = line[1]
        number = name.partition(" ")[0]
        table_string = """|| [[[minor-planets:"""+ number +""" |"""+ name +"""]]] || """+ meaning +""" ||\n"""
        final_table += table_string
    print(final_table)
    
    #5. edit wiki page to have that content
    title = "List " + str(startnum) + "-" + str(endnum)
    try:
        #api.server.pages.save_one({"site": api.Site, "page": listpage, "title": title, "content": preamble + final_table + postamble})
        api.refresh_pages()
    except:
        print("Failed to update page :(") #idk


#https://en.wikipedia.org/w/api.php?action=parse&page=Meanings_of_minor_planet_names%3A_4001%E2%80%935000&prop=text&formatversion=2&format=json


if __name__ == "__main__":
    #main("list:12001-150000",['OSIRIS-REx'])
    #main("list:1-700000",['Astronaut','astronaut','cosmonaut','taikonaut','STS-'])
    main("list:1-700000",['Astronomer','astronomer'])
    """
    main("list:4001-5000") #997
    main("list:5001-6000") #890
    main("list:6001-7000") #844
    main("list:7001-8000") #769
    main("list:8001-9000") #771
    main("list:9001-10000") #736
    main("list:10001-11000") #728
    main("list:11001-12000") #589
    main("list:12001-13000") #586
    main("list:13001-14000") #430
    main("list:14001-16000") # 701
    main("list:16001-18000") # 677
    main("list:18001-20000") # 681
    main("list:20001-22000") # 847
    main("list:22001-24000") # 702
    main("list:24001-26000") # 735
    main("list:26001-28000") # 614
    main("list:28001-30000") # 585
    main("list:30001-32000") #600
    main("list:32001-35000") #732
    main("list:35001-40000") #259
    main("list:40001-70000") #838
    main("list:70001-100000") #618
    main("list:100001-150000") #869
    main("list:150001-200000") #619
    main("list:200001-300000") #894
    main("list:300001-400000") #458
    main("list:400001-700000") #253
    """


