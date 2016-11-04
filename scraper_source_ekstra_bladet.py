import requests
import sys
from bs4 import BeautifulSoup
import time
import Story
import pymongo
from pymongo import MongoClient
from datetime import datetime
import time
from termcolor import colored



# CONNECT TO MONGODB
client = MongoClient('mongodb://127.0.0.1:27017/xxxxxx')
db = client.newsdiff

list = []

# SUPPLY URL SCOPE TO REQUESTS
r = requests.get("http://ekstrabladet.dk/nyheder/")

# FEED REQUESTS CONTENT TO BEAUTIFULSOUP PARSER
soup = BeautifulSoup(r.content, 'html.parser')

links = soup.find_all("div", {'class' : 'listline'})
cc = 0

print colored('*****************************************', "red")
print colored("RUNNING SCRAPE - " + time.strftime("%c"), "green")
print colored('*****************************************', "red")

# FIRST GET ALL LINKS MATCHING THE ACCEPTED PATTERN
for link in links:
	url = link.find('a').get('href')
	title = link.find('a').get('title')
	if "http://ekstrabladet.dk/nyheder/" in url:
		if len(url) > 60:
			list.append(url)

time.sleep(0.2)

cnt = 0

# NEXT. VISIT EACH LINK TO FETCH ARTICLE TITLE AND CONTENT

for i in list:

	title = ""
	link = i
	content = ""

	n = requests.get(i)
	more_soup = BeautifulSoup(n.content, 'html.parser')
	article_title = more_soup.find_all("div", {'class' : 'headercontainer'})
	for h1 in article_title:
		tit = h1.find("h1").text
		title = tit[9:]
		article_content = more_soup.find_all("div", {'class' : 'bodytext'})
		for p in article_content:
			p_list = p.find_all("p")

			for item in p_list:
				if(len(item.text) > 40):
					content += item.text
					content += " \n "
	time.sleep(0.2)
	query = db.stories.find_one({ "link": link })

	# try:
	results = db.stories.update(
        {'_id': link }, {
                '$set': {
#                         "_id": link,
                  "title": title,
                  "link": link,
                  "content": content,
                  "created_at": time.strftime("%c")
          }
         }, upsert = True)


	print colored ("." * cnt, "red")
	cnt += 1
	if(cnt == len(list)):
		break

print colored(" - ALL DONE ! - ", 'green')
