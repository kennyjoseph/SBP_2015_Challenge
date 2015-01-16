Intro
======

This Github repository will serve as the hub for data and code distributed by the heads of and used by the participants of the [2015 SBP Challenge Problem](http://sbp-conference.org/challenge/). 

We welcome any additions to this repository at any time, fork and submit a pull request or shoot one of us an email and we can work something out if you're not very familiar with git/Github.

Tweet Hydrator
==============

The first thing in this repository is a set of python scripts in the ```tweet_hydrator``` directory.  
In here, you will find a script ```tweet_getter.py``` that is able to take in a set of tweet ids and produce JSON files 
that hold the full information for all tweets in the list of IDs that are still publicly available.

For the purposes of the Challenge problem, two relevant sets of tweet IDs has already been added.  
1. The tweet IDs for #GamerGate that Andy Baio shared and used in 
[his analysis on Medium.com](https://medium.com/message/72-hours-of-gamergate-e00513f7cf5d) are in the file ```data/gamergate_tweet_ids.csv```.
2. Tweet IDs for tweets relevant to the 2014 protest activity in Ferguson, Missouri. The file contains 1.1M tweets ids from 7-14 days after the first protests. These ids are in the (gzipped) file ```data/ferguson_tweet_ids.txt.gz```.

To pull down these tweets, you can run the script in the following manner:

```
> python tweet_getter.py [output_dir] [tweet_id_file]
```

The script thus takes two arguments. The first argument is the output directory for the JSON for the hydrated tweets. 
The second is a file that has one tweet id per line. In this case it would be ```gamergate_tweet_ids.csv```.

To make the code run, you'll actually have to change two lines of code within the script.  The first is:
```
app_info = ['APP_KEY_1','APP_SECRET_1']
```

You'll have to replace ```APP_KEY_1``` with a Twitter application key and ```APP_SECRET_1``` with a Twitter application secret
 (note: it's called a secret for a reason, so make sure not to share it!). To create an application, head over to 
 [the Twitter apps page](https://apps.twitter.com/) and register one.  Once you do, go to the "Keys and Access Tokens"
 tab of the Application Management screen, and replace ```APP_KEY_1``` with your "Consumer Key (API Key)" and
 ```APP_SECRET_1``` with your "Consumer Secret"
 
You'll also have to change the following line:

```
users = ['kjoseph5']
```

Replace the (my) Twitter handle there with your own, and your friends if you can steal their password (kidding!).

Now, you can run the script. The first time you do,  the script will request that you visit a URL in your browser 
to allow it authorize the usernames you provided to your application. Get the PIN from the URL (after you log in
with that user) and enter it on the command line where you ran the script.  The script generates a config
file from this information (in the same directory where the script was run, with the app key as the name) 
so you don't have to do it every time you start it up, but you are always welcome 
to delete this file so you don't have that information hanging around.

Your output will be a series of .json files in your output directory. Happy analyzing!

License
=========
All code in this repository follows the MIT License agreement.

```
The MIT License (MIT)

Copyright (c) 2014 Kenneth Joseph, Peter M. Landwehr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
