import tweepy
import json
#from userschema import *
import useracess 
import time
import logging
import logging.config

class Twitter(object):
    def __init__(self,handle):
        self._api = None
        self._endpoint = None
        self._message=None
        u = UserAccess();
        auth = tweepy.OAuthHandler(u.getConsumerKey(handle),u.getConsumerSecret(handle))
        auth.set_access_token(u.getAccessToken(handle),u.getAccessTokenSecret(handle))
        self._api = tweepy.API(auth)

    @property
    def api(self):
        """I'm the 'api' property."""
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @api.deleter
    def api(self):
        del self._api

    def debug(method):
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            elapsed = str(float(te - ts))
            logger = logging.getLogger(__name__)
            logger.debug(str(args) + '. Elapsed time - ' + str(elapsed) + ' secs.')
            return result
        return timed

    def wait(self,secs):
        if secs == 0:
            return
        logging.warning('Limit reached. Waiting for ' + str(secs) + ' seconds.')
        time.sleep(secs)

    def getRateLimit(self,rate_data,endpoint):
        return rate_data['resources'][endpoint.split('/')[1]][endpoint]['limit']

    def getRemaining(self,rate_data,endpoint):
        return rate_data['resources'][endpoint.split('/')[1]][endpoint]['remaining']

    def getResetTime(self,rate_data,endpoint):
        return rate_data['resources'][endpoint.split('/')[1]][endpoint]['reset']

    def check_rate_to_wait(self,rate_data):
        # Rate_limit_Status endpoint
        rate_limit_endpoint = '/application/rate_limit_status'

        endpoint_limit = self.getRateLimit(rate_data,self._endpoint)
        rate_check_limit = self.getRateLimit(rate_data,rate_limit_endpoint)
        endpoint_remain = self.getRemaining(rate_data,self._endpoint)
        rate_check_remain = self.getRemaining(rate_data,rate_limit_endpoint)
        endpoint_reset_time = self.getResetTime(rate_data,self._endpoint)
        rate_check_reset_time = self.getResetTime(rate_data,rate_limit_endpoint)

        # Wait if the remaining limit is less than 10% of total limit
        threshold = 0.1
        if (endpoint_remain <= endpoint_limit * threshold):
            self.wait(endpoint_reset_time - int(time.time()) + 1)

        if (rate_check_remain <= rate_check_limit * threshold):
            self.wait(rate_check_reset_time - int(time.time()) + 1)

###### TWITTER PUBLIC API START ##################################################
    def rate_limit_status(self):
        rate_data = self._api.rate_limit_status()
        self._endpoint = '/application/rate_limit_status'
        self.check_rate_to_wait(rate_data)

##################################################################################
