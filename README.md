# bibliomania

This Python code opens and slices an ebook and then posts it sequentially to Twitter with a hashtag. The app uses Tweepy for twitter authorization and Beautiful Soup for text parsing. A cron job handles the scheduling of tweets, and a blob in a Google Cloud storage bucket keeps track of the character count for determining where to start the next slice of text. Twitter credentials go in a separate file, hidden.py (not included here).

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The thought, however, was a<br>good one; and many of the<br>heads are powerfully executed.<a href="https://twitter.com/hashtag/bibliomania1809?src=hash&amp;ref_src=twsrc%5Etfw">#bibliomania1809</a></p>&mdash; Bookish Bot (@BotBookish) <a href="https://twitter.com/BotBookish/status/1366119312533110786?ref_src=twsrc%5Etfw">February 28, 2021</a></blockquote>

The code can open, slice, and post text from any text or html file, but the envisioned purpose is to renew attention to forgotten literary works in the public domain by posting bite-sized excerpts to a social media platform. The example used here is Project Gutenberg's text edition of Thomas F. Dibdin's 1809 *Bibliomania; or Book Madness*.

License: Creative Commons BY-SA 4.0
