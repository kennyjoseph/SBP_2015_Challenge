"""
    This class handles a Twitter session. It needs an OAuth1Service in order to handle
    connection errors, which are unfortunately pretty frequent.
"""
from rauth import OAuth1Service
import requests, simplejson
from time import sleep


class TwitterAPIHook:

    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, session):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET

        ##FOR RECONNECTIONS
        self.twitter = OAuth1Service(
            name='twitter',
            consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            base_url='https://api.twitter.com/1.1/')

        self.session = session

    def call_to_api(self, url, params, name=""):
        request_completed = False
        tried_request = 0
        while not request_completed:
            try:
                tried_request += 1
                r = self.session.get(url, params=params, verify=True)
                r.json()
                request_completed=True
            except requests.exceptions.ConnectionError:
                print 'connection error! Sleeping for 60 then reconnecting ', name, ' request tries: ', tried_request
                print self.session.access_token, self.session.access_token_secret
                sleep(60)
                try:
                    self.session = \
                        self.twitter.get_session((self.session.access_token, self.session.access_token_secret))
                except:
                    print 'FAILED RECONNECT AGAIN!!'
                print ' reconnected: ', name
            except simplejson.decoder.JSONDecodeError:
                print ' JSON ERROR! ', name
                if tried_request > 2:
                    print ' could not recover from JSON error, continuing ', name
                    return None

        if 'errors' in r.json():
                print ' errors: ', r.json()['errors'][0]['message'], ' URL: ', url,  ' params: ', params
                if r.json()['errors'][0]['code'] != 34:
                    print 'SLEEPING'
                    sleep(5*60)
                else:
                    return None
        elif 'error' in r.json():
                ## error handling
                reason = r.json()['error']
                print '\tGot an error, reason: {0} URL: {1} params: {2}'.format(reason, url, params)
                return None

        return r

    def get_from_url(self, url, params):
        return self.call_to_api(url, params, "no_name").json()

    def get_user_params(self, params, screen_name, user_id):
        if screen_name is not None:
            params['screen_name'] = screen_name
            return
        if user_id is not None:
            params['user_id'] = user_id
            return
        raise Exception('No user info provided', 'Please provide user info')

    def get_with_cursor_for_user(self, url, json_payload_name, screen_name=None, user_id=None, params=None):
        if params is None:
            params = {}
        self.get_user_params(params, screen_name, user_id)
        params['cursor'] = -1

        data = []
        while True:
            sleep(70)
            r = self.call_to_api(url, params)
            if r is None:
                break
            json_data = r.json()
            data += json_data[json_payload_name]
            if json_data['next_cursor'] == 0:
                break
            params['cursor'] = json_data['next_cursor']

        return data

    def get_with_max_id_for_user(self, url, params, screen_name, user_id, name=""):
        self.get_user_params(params, screen_name, user_id)
        data = []
        while True:
            sleep(6)
            r = self.call_to_api(url, params, name)
            if r is None:
                break
            try:
                if len(r.json()) == 0:
                ##finished user
                    break
                
                if 'id' in r.json()[-1]:
                    params['max_id'] = r.json()[-1]['id']-1
                else:
                    print 'no max id!!!'
                data += r.json()
            
            except:
                print ' CALL FAILED, JSON COULD NOT PARSE: ', url, params, name
                break

        return data
