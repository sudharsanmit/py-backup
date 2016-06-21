import tweepy
import json
from pattern.en import referenced

consumer_key = 'Q3EUZhyXATaWldXq9z58gplxn'
consumer_secret = 'bjyWhEX6HlysAyh4ZQIyNMLdIBLjHJuEcyh2DnhPgXI85ych5D'
access_token = '2838429686-anjg7364jCOKR9GuXy0metbqP8S3o7XOa8LHob5'
access_token_secret = 'iak0s5Zy8w01CXpZhdTe5Sqi7TnQCWeqnPXxA4iMnNgpc'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
 
# Sample method, used to update a status
#api.update_status('Hello World from Python!')

user = api.me()
 
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))
print (user)
