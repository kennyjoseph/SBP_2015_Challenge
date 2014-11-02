Intro
======

This Github repository will serve as the hub for data and code distributed by the heads of and used by the participants of the [2015 SBP Challenge Problem](http://sbp-conference.org/challenge/). 

We welcome any additions to this repository at any time, fork and submit a pull request or shoot one of us an email and we can work something out if you're not very familiar with git/Github.

Tweet Hydrator
==============

The first thing in this repository is set of python scripts in the ```tweet_hydrator``` directory.  In here, you will find a script ```tweet_getter.py``` that is able to take in  a set of tweet ids and produce JSON files that hold the full information for all of the tweets in that list which are still publically available.

For this to work, you'll also need a Twitter application and at least one registered accounts for that application.  To get that, head over to [the Twitter apps page](https://apps.twitter.com/) and register an account.

For the purposes of the Challenge problem, a relevant set of tweet IDs has already been added.  The tweet IDs for #GamerGate that Andy Baio shared and used in [his analysis on Medium.com](https://medium.com/message/72-hours-of-gamergate-e00513f7cf5d) are in the file ```gamergate_tweet_ids.csv```.

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