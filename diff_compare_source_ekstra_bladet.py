import requests
import sys
from bs4 import BeautifulSoup
# import MySQLdb
from random import randint
import time
import Story
import pymongo
from pymongo import MongoClient
from datetime import datetime
import time
from termcolor import colored
import difflib


# CONNECT TO MONGODB
client = MongoClient('mongodb://127.0.0.1:27017/newsdiff')
db = client.newsdiff

list = []
content = ""

print colored("\n -----------------------------", "yellow")
print colored("\t -  G O !  -", "green")
print colored("\n     -  DIFF COMPARE  -", "blue")
print colored("\n -----------------------------", "yellow")

d = difflib.Differ()


# GET LIST OF LINKS TO CHECK FOR CHANGES


for i in db.stories.find():
	if "http://ekstrabladet.dk/nyheder/" in i:
		list.append(i.values())

for it in list:
	print colored('FOLLOWING LINK: ', 'blue')
	print colored(it[2], 'magenta', attrs=['blink'])
	print("\n")

	r = requests.get(it[2])

	soup = BeautifulSoup(r.content, 'html.parser')
	article_content = soup.find_all("div", {'class' : 'bodytext'})


	for p in article_content:
		p_list = p.find_all("p")

		for item in p_list:
			if(len(item.text) > 40):
				content += item.text
				content += " \n "

	time.sleep(1)
	listing = []

	text1_lines = it[0].splitlines()
	text2_lines = content.splitlines()

	diff = d.compare(text1_lines, text2_lines)

	listing.append('\n'.join(diff))

	set_pre = set(it[0].split(' '))
	set_post = set(content.split(' '))

	if set_pre != set_post:
		pre_string = it[0].encode('utf-8')
		post_string = content.encode('utf-8')
		print(post_string)
		print colored("DIFF FOUND", "yellow")
		content = ""
		results = db.difffound.insert_one(
			{
				  "title": it[4],
				  "link": it[2],
				  "difflib": listing[0],
				  "content_pre": pre_string,
				  "content_post": post_string,
				  "time_scrape": it[1],
				  "time_diff": time.strftime("%c")
		 	  }
		 )
		time.sleep(1)
	else:
		print colored("NO DIFF", "green")
		content = ""
