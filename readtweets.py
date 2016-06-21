import tweepy
import json
import twitter_auth

api = twitter_auth.api


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print ('Sleeping')
            time.sleep(15 * 60)
        except other:
            raise

readuser="udottraffic"

for tweet in limit_handled(tweepy.Cursor(api.user_timeline, readuser).items()):
    try:
        #print (tweet.text) 
        #print (tweet.text, tweet.source)
        list = tweet.text.splitlines ()
        print (list)
    except:
        print ('')
        


#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#   try:
#    print (tweet.text)
#   except:
#       print ('Unable to print')
