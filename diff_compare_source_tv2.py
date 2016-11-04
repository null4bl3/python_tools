import requests
import sys
from bs4 import BeautifulSoup
# import MySQLdb
import difflib
from random import randint
import time
import Story
import pymongo
from pymongo import MongoClient
from datetime import datetime
import time
from termcolor import colored

# CONNECT TO MONGODB
client = MongoClient('mongodb://127.0.0.1:27017/newsdiff')
db = client.newsdiff

list = []
tmp_list = []
content = ""

print colored("\n -----------------------------", "yellow")
print colored("\n \t -  G O !  -", "green")
print colored("\n     -  DIFF COMPARE  -", "blue")
print colored("\n         -  TV2  -", "magenta")
print colored("\n -----------------------------", "yellow")

# GET LIST OF LINKS TO CHECK FOR CHANGES
# wait = randint(0,59)
# print(wait)
# time.sleep(wait)

for i in db.stories.find():
	tmp_list.append(i.values())
#

for t in tmp_list:
	url_tmp = t[2]
	if url_tmp[:22] == "http://nyheder.tv2.dk/":
		list.append(t)

for it in list:
	print colored('FOLLOWING LINK: ', 'blue')
	print colored(it[2], 'magenta', attrs=['blink'])
	print("\n")

	# print(it[2])
# 	# print(it[4])
	r = requests.get(it[2])
	more_soup = BeautifulSoup(r.content, 'html.parser')

	article_content = more_soup.find_all("div", {'class' : 'o-article_body'})
	for p in article_content:
		p_list = p.find_all("p")

		for item in p_list:
			if(len(item.text) > 40):
				content += item.text
				content += " \n "

	time.sleep(1)


	d = difflib.Differ()
	first = it[0]
	second = content

	# listing = []
	#
	# text1_lines = it[0].splitlines()
	# text2_lines = content.splitlines()
	#
	# diff = d.compare(text1_lines, text2_lines)
	#
	# listing.append('\n'.join(diff))

	set_pre = set(it[0].split(' '))
	set_post = set(content.split(' '))

	if set_pre != set_post:
		listing = []

		text1_lines = it[0].splitlines()
		text2_lines = content.splitlines()

		diff = d.compare(text1_lines, text2_lines)

		listing.append('\n'.join(diff))

		pre_string = it[0].encode('utf-8')
		post_string = content.encode('utf-8')
		# print(post_string)
		print colored("DIFF FOUND", "yellow")
		print(listing[0])
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


print(listing)
