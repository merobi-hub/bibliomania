# [START gae_flex_quickstart]

from wsgiref import headers
from flask import Flask
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import textwrap
from var import index
from hidden import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
from tweepy import TweepError
#from thisapp.wsgi import application

#app = application
app = Flask(__name__)

@app.route('/')

# Ignore SSL certificate errors
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE



# TEXT STATS:
# length of cleantext = 1831990
# start_pos = 4135
# len - start_pos = 1827855
# note: use 1827855 as terminus

# Sign in to Twitter using Tweepy
def auth():
    auth = tweepy.OAuthHandler(hidden.consumer_key, hidden.consumer_secret)
    auth.set_access_token(hidden.access_token, hidden.access_token_secret)
    return tweepy.API(auth)
try:
    api = auth()
    print('Auth status: success')
except:
    print('Auth status: failure')

chunk_wrp = 'None'

# Create first or next chunk of text to post and post tweet
def get_chunk():
    print('get_chunk attempted')
    got_chunk = False
    tag = ' #bibliomania1809'
    for chunk in cleantext:
        chunk = cleantext[index:index + 262]
        chunk = chunk + tag
        new_chunk = textwrap.fill(chunk)
        got_chunk = True
        if new_chunk is not None:
            break
    chunk_wrp = new_chunk
    print('Chunk_wrp: ', chunk_wrp)
    print('Index: ', index)
    if got_chunk:
        new_index = index + 262
        update = False
        with open('var.py', 'w+') as f:
            f.write(f'index = {new_index}')
            f.close()
            update = True
        print('New index: ', new_index)
    if update:
        print('attempting tweet')
        try:
            #api.update_status('test')
            api.update_status(chunk_wrp)
            print('status updated')
        except:
            print('Status update failed')

get_chunk()   

def web_output(environ, start_response):
    body = '<center><p><h1>Bibliomania</h1></p>
    <a class="twitter-timeline" href="https://twitter.com/BotBookish?ref_src=twsrc%5Etfw">Tweets by BotBookish</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </center>' 
    status = '200 OK'
    headers = [('Content-type', 'html')]
    start_response(status, headers)
    return [body.encode('utf-8')]

#get and tweet the chunk:
get_chunk()

#output to web:
web_output(environ, start_response)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host=gunicorn -b :$PORT main:app, debug=True)

('/')
# [END gae_flex_quickstart]
