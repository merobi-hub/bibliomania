# bibliomania

This Python code opens and slices html and then posts it sequentially to twitter with a hashtag. The app uses Tweepy for twitter authorization and Beautiful Soup for text parsing. A cron job handles the scheduling of tweets, and a separate file (var.py) keeps track of the character count for determining where to start the next slice of text. Twitter credentials go in a separate file, hidden.py (not included here).

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">ublished the Physiognomical Portraits, a performance not divested of<br>interest—but failing in general success, from the prints being, in<br>many instances, a repetition of their precursors. The thought,<br>however, was a good one; and many of the heads are powerfu<a href="https://twitter.com/hashtag/bibliomania1809?src=hash&amp;ref_src=twsrc%5Etfw">#bibliomania1809</a></p>&mdash; Bookish Bot (@BotBookish) <a href="https://twitter.com/BotBookish/status/1334941991549984770?ref_src=twsrc%5Etfw">December 4, 2020</a></blockquote> 

The code can open, slice, and post text from any html file, but the envisioned purpose is to renew attention to forgotten literary works in the public domain by posting bite-sized excerpts to a social media platform. The example used here is Project Gutenberg's html edition of Thomas F. Dibdin's 1809 *Bibliomania; or Book Madness*.

# status and issues

Development faces some execution issues, and the code can currently be run only from the command line. The objective is to house the app on Gcloud in a standard Python 3 environment. Web output is simply the twitter account's timeline. The most recent attempt to run the app on Gcloud produced the following error message:

Updating service [default] (this may take several minutes)...failed.
ERROR: (gcloud.app.deploy) Error Response: [9] 
Application startup error! Code: APP_CONTAINER_CRASHED
/bin/sh: 1: exec: gunicorn: not found

