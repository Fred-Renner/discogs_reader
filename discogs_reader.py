import httplib2 
import requests
import re
import collections
from bs4 import BeautifulSoup, SoupStrainer
import time

# enter minmum ratio of want to have: want/have
target_minimum_ratio = 2

# get link_list of html adresses of displayed records on the website

discogs_search_webpage='https://www.discogs.com/search/?sort=have%2Cdesc&type=all&style_exact=Trance'

http = httplib2.Http()
status, response = http.request(discogs_search_webpage)

link_should_contain     = ["release", "master"]
link_should_not_contain = ["search", "seller","add?","sort=have"]
link_list=[]

for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
    if link.has_attr('href'):

        final_link = link.get('href')
        contained = any(x in final_link for x in link_should_contain)
        not_contained = not (any(x in final_link for x in link_should_not_contain))

        if contained & not_contained : 
            
            link_list.append(final_link)

link_list=([item for item, count in collections.Counter(link_list).items() if count > 1])

for link in link_list:
    print(link)

# extract links with selection
selected_links=[]
for link in link_list:

    link = "https://www.discogs.com" + link

    status, response = http.request(link)
    soup = BeautifulSoup(response, features="html.parser")


    have = soup.find_all("a", class_="coll_num")
    have = re.search('>(.*)</a>', str(have))
    want = soup.find_all("a", class_="want_num")
    want = re.search('>(.*)</a>', str(want))
    have = float(have.group(1))
    want = float(want.group(1))

    print(have/want)
    if have/want >= target_minimum_ratio:
        #selected_links.append(selected_links)
    
        print(link)


