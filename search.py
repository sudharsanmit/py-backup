import urllib
import tweepy
import json
import twitter_auth

#api = twitter_auth.api
twitter = twitter_auth.authorize("sudharsanmit")


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
        except other:
            raise

# Like method
def like():
    print ("TODO");

# Retweet method
def retweet():
    print ("TODO");

# Tweet method
def tweet():
    print ("tweet")

# Follow method
def follow():
    print ("TODO")

# Search method
def search():
    print ("TODO");

# Get followers
def getFollowers():
    print ("TODO");

# Master's command
def masterCmd():
    print ("TODO");


        #api.update_status(status="Thank you for the info.@<tweet.screen_name>", in_reply_to_status_id=tweet.id)


# Main method
def main():
    print ("Hi");

if __name__ == '__main__':
    main()

