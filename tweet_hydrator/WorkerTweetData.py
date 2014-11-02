__author__ = 'kjoseph'

import multiprocessing
import sys,traceback, codecs
import simplejson as json
from time import sleep

class TweetDataWorker(multiprocessing.Process):
    def __init__(self, queue,api_hook, conn_number, out_dir,to_pickle=False,gets_user_id=True):
        multiprocessing.Process.__init__(self)
        self.queue= queue
        self.api_hook = api_hook
        self.conn_number = conn_number
        self.out_dir = out_dir
        self.to_pickle = to_pickle
        self.gets_user_id = gets_user_id
        self.tweet_output_file = codecs.open(self.out_dir+"/"+str(conn_number)+".json","a","utf-8")

    def run(self):
        print 'Worker started'
        # do some initialization here

        for data in iter( self.queue.get, None ):
            sleep(10)
            try:
                if data == None:
                    print 'ALL FINISHED!!!!', self.conn_number
                    self.tweet_id_output_file.close()
                    self.tweet_output_file.close()
                    break

                print 'Starting: ', data[1]


                tweet_data = self.api_hook.get_from_url("statuses/lookup.json",
                                                       {"id":",".join(data)})

                data = set([int(d) for d in data])
                good = 0
                for tw in tweet_data:
                    good += 1
                    self.tweet_output_file.write(json.dumps(tw)+"\n")
                    data.remove(tw['id'])


                print 'N GOOD: ', good

            except Exception:
                print 'FAILED:: ', data
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print "*** print_tb:"
                traceback.print_tb(exc_traceback, limit=30, file=sys.stdout)
                print "*** print_exception:"
            #print 'finished collecting data for: ', data.pop()

