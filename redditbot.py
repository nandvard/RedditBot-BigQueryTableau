import praw


r = praw.Reddit('bot')


submissions = r.subreddit('funny').hot(limit=1)


for s in submissions:

	s.reply("test")
	#print (s.title)
