import httplib2 
import re
import collections
from bs4 import BeautifulSoup, SoupStrainer
import time


# enter minomum ratio of want to have: want/have
target_minimum_ratio = 2

# discogs token
token = "nDPMjQBFGRcgQHkXNZUjBhRlNnMusnodhlTndQZh"

# get release_list of html adresses of displayed records on the website
discogs_search_webpage='https://www.discogs.com/search/?limit=250&sort=want%2Cdesc&ev=em_rs&style_exact=House&style_exact=Tech+House&decade=1990&page=1'

# check if pages exist
if "page" not in discogs_search_webpage:
    discogs_search_webpage += "&page=1"

# how many search pages
pages_begin = 3
pages_stop =  5

release_list=[]
link_should_contain     = ["release", "master"]
#link_should_contain     = ["release"]
#link_should_contain     = ["master"]
link_should_not_contain = ["search", "seller","add?","sort=have"]   

for page in [1]:
    

    link_elements = discogs_search_webpage.split("=")
    link_elements[-1] = str(page) 
    discogs_search_webpage = "=".join(link_elements)

    http = httplib2.Http()
    print(discogs_search_webpage)
    status, response = http.request(discogs_search_webpage)

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            
            final_link = link.get('href')
            contained = any(x in final_link for x in link_should_contain)
            not_contained = not (any(x in final_link for x in link_should_not_contain))
            
            if contained & not_contained :         
               #release_list.append( final_link.split("/")[-1] )
               release_list.append( final_link )


# sort out doubles
release_list=([item for item, count in collections.Counter(release_list).items() if count > 1])

for release in release_list:
    print(release)

for rel in release_list:

    link_elements = rel.split("/")
    release_id = link_elements[-1]
    if "release" in link_elements:
        link = "https://www.discogs.com/release/stats/" + release_id 
    elif "master" in link_elements:  
        link = "https://www.discogs.com/master/stats/" + release_id

    print(link)
    status,response = http.request(link)
    #print(response)
    soup = BeautifulSoup(response, features="html.parser")
    soup.find(string=re.compile("members have this"))
    #soup.find_all("h3").index("members have this")
    have_want_raw = list(soup.find_all("h3"))
    #print(type(have_want_raw))
    #print("members" in str(have_want_raw[3]))

    
    for i in have_want_raw:
        print(type(i))
        stat_str = str(i)
        print(stat_str)
        if "members have this" in stat_str:
            stat_str = stat_str.split(" ")
            have=float(stat_str[stat_str.index("members")-1])
        elif "members want this" in stat_str:
            stat_str = stat_str.split(" ")
            want=float(stat_str[stat_str.index("members")-1])    
    print(want/have)
    

    if want/have >= target_minimum_ratio:
        #selected_links.append(selected_links)
    
        print(link)

""" for rel in release_list:
    
    #link = "https://www.discogs.com" + rel 

    #link = "https://api.discogs.com/releases/stats" + rel 
    status,response = http.request(link)
    print(response)

    time.sleep(1)

    #https://www.discogs.com/release/stats/80571#collection
    
    soup = BeautifulSoup(response, features="html.parser")
    print(response)
    have = soup.find_all("a", class_="coll_num")
    print(have)
    have = re.search('>(.*)</a>', str(have))
    

    want = soup.find_all("a", class_="want_num")
    want = re.search('>(.*)</a>', str(want))
    have = float(have.group(1))
    want = float(want.group(1))

    print(have/want)

    if have/want >= target_minimum_ratio:
        #selected_links.append(selected_links)
    
        print(link)


 """