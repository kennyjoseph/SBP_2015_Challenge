__author__ = 'kjoseph'

'''
This script is the main script you'll use to hydrate tweets -it uses the other files

Sorry its not very formal, but I'll slowly be updating this public release with the more stable
tools we're developing internally

This script takes four arguments (not even using argparse yet, so its just an ordered set of arguments...sorry...)

The first argument is a file that gives Twitter API credentials.
the format of the file is pretty simple.
the first line should be:
APP_KEY,APP_SECRET
followed by any number of lines representing authenticated users to the app, in the form:
USERNAME,TOKEN,SECRET

note that you can actually have multiple files of this kind without much excess effort

The second argument is the output directory for the hydrated tweets

The third is a file that has one tweet id per line

'''

import os, sys, time
from multiprocessing import Manager
from TwitterApplicationHandler import TwitterApplicationHandler
from WorkerTweetData import TweetDataWorker


if len(sys.argv) != 4:
    print 'usage:  [app_information_file] [output_dir] [tweet_id_file]'
    sys.exit(-1)


APPLICATION_INFORMATION_FILENAME = sys.argv[1]
OUTPUT_FILENAME = sys.argv[2]
INPUT_FILENAME = sys.argv[3]

### get authenticated handles we can use to pull tweets
app_handler = TwitterApplicationHandler(pathToConfigFile=APPLICATION_INFORMATION_FILENAME)
handles = app_handler.api_hooks
print 'n accounts to be used: ', len(handles)

##get the tweet ids to use - for the gamergate file, there is a header line and
## user ids, both of which we ignore
input_file = open(INPUT_FILENAME)
input_file.readline()
tweet_ids = [line.split(",")[0].strip() for line in input_file]
input_file.close()

##Create the output directory
try:
    os.mkdir(OUTPUT_FILENAME)
except:
    pass

print 'num tweets to get: ', len(tweet_ids)

#chunk tweets into 100s ... really, could use numpy here but don't really need that dependency
i = 0
tweets_chunked = []
while i < len(tweet_ids):
    tweets_chunked.append(tweet_ids[i:(i+100)])
    i += 100
tweets_chunked.append(tweet_ids[i-100:len(tweet_ids)])

request_queue = Manager().Queue()
for tweet_chunk in tweets_chunked:
    request_queue.put( tweet_chunk )

print 'all tweets added, n chunks: ', len(tweets_chunked)

for i in range(len(handles)):
    time.sleep(10)
    TweetDataWorker(request_queue,handles[i],i,OUTPUT_FILENAME).start()

# Sentinel objects to allow clean shutdown: 1 per worker.
for i in range(len(handles)):
    request_queue.put( None )

print 'finished'