import praw
import config 
import time
import os
import requests

def bot_login():
	print("Trying to loggin..............")
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Random jokes"
			)

	print("Logged in.")

	return r



def run_bot(r, comment_replied_to):
	print("obtaining 30 comments........")

	for comment in r.subreddit('test').comments(limit=30):
		if "!jokes" in comment.body and comment.id not in comment_replied_to and comment.author != r.user.me():
			print("string with \"!joke\" found " + comment.id)

			comment_reply = "You requested a joke! Here it is:\n\n"
			joke = requests.get('http://api.icndb.com/jokes/random').json()['value']['joke']

			comment_reply += ">" + joke
			comment_reply += "\n\n This joke came from [ICNDb.com](http://api.icndb.com)."
			comment.reply(comment_reply)
			print("replied to comment" + comment.id)
			comment_replied_to.append(comment.id)


			with open ("comment_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")




	print (" Sleeping for 10 seconds....")
	time.sleep(10)


def get_saved_comments():
	if not os.path.isfile("comment_replied_to.txt"):
		comment_replied_to = []
	else:
		with open("comment_replied_to.txt", "r") as f:
			comment_replied_to = f.read()
			comment_replied_to = comment_replied_to.split("\n")
			#comment_replied_to = filter(None, comment_replied_to)

	return comment_replied_to


r = bot_login()
comment_replied_to = get_saved_comments()
print(comment_replied_to) 

while True:
	run_bot(r, comment_replied_to)
