__author__ = 'kjoseph'
import os, sys, time,signal
from multiprocessing import Manager
from TwitterApplicationHandler import TwitterApplicationHandler
from WorkerTweetData import TweetDataWorker
from multiprocessing.managers import SyncManager

if len(sys.argv) != 3:
    print 'usage:  [output_dir] [tweet_id_file]'
    sys.exit(-1)

app_info = ['APP_KEY_1','APP_SECRET_1']

users = ['kjoseph5']

### get authenticated handles we can use to pull tweets

handler = TwitterApplicationHandler(consumer_key=app_info[0],consumer_secret=app_info[1])
for user in users:
    handler.init_new_user(user)
handles = handler.api_hooks
print 'n accounts to be used: ', len(handles)


OUTPUT_FILENAME = sys.argv[1]
INPUT_FILENAME = sys.argv[2]

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

#chunk tweets into 100s
i = 0
tweets_chunked = []
while i < len(tweet_ids):
    tweets_chunked.append(tweet_ids[i:(i+100)])
    i += 100
tweets_chunked.append(tweet_ids[i-100:len(tweet_ids)])



#handle SIGINT from SyncManager object
def mgr_sig_handler(signal, frame):
    print 'not closing the mgr'

#initilizer for SyncManager
def mgr_init():
    signal.signal(signal.SIGINT, mgr_sig_handler)
    print 'initialized mananger'

#using syncmanager directly instead of letting Manager() do it for me
manager = SyncManager()
manager.start(mgr_init)

request_queue = Manager().Queue()
for tweet_chunk in tweets_chunked:
    request_queue.put( tweet_chunk )

print 'all tweets added, n chunks: ', len(tweets_chunked)

# Sentinel objects to allow clean shutdown: 1 per worker.
for i in range(len(handles)):
    request_queue.put( None )


processes = []
for i in range(len(handles)):
    p = TweetDataWorker(request_queue,handles[i],i,OUTPUT_FILENAME)
    p.start()
    processes.append(p)

try:
    for p in processes:
        p.join()
except KeyboardInterrupt:
    print 'keyboard interrupt'
print 'finished'