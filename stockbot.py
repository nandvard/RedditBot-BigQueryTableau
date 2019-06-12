import praw             #Reddit API
import pymysql          #AWS mySQL API
import rdsconfig        
import re
import datetime
import pandas_datareader as pdr #Stock API


def lambda_handler(event,context):
        date = datetime.datetime(2019, 5, 9)
        datestr = date.strftime('%Y-%m-%d')
        stock = pdr.data.DataReader('COF', 'iex', date, date)   #Closing price on 5/9/2019
        price = stock.loc[datestr]['close']

        conn = pymysql.connect(rdsconfig.host, rdsconfig.user, rdsconfig.passwd, rdsconfig.db)  
        cur = conn.cursor()

        r = praw.Reddit('bot')

        for post in r.subreddit('test').new(limit=10):          #Get new posts
            if re.search("stock", post.title, re.IGNORECASE):   #Search keyword 'stock'
                pid = post.id

                sql1 = "select 1 from posts where id = %s"      #Avoid repeats
                cur.execute(sql1,pid)

                if cur.rowcount == 0:
                    print (pid)
                    post.reply(datestr+" COF close $"+str(price))       #Comment stock price
                    post.upvote()

                    sql2 = "insert into posts(id) values(%s)"           #Track post
                    cur.execute(sql2,pid)
                    conn.commit()

        conn.close()

#lambda_handler(0,0)
