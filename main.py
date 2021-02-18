import datetime
from flask import Flask, render_template, request, jsonify
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import textwrap
from hidden import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
from tweepy import TweepError
import sys
import requests
import signal
import os

app = Flask(__name__, template_folder = 'templates')
app.config.update(
    SERVER_NAME = "127.0.0.1:8080"
    #SERVER_NAME = "bibliomania.nn.r.appspot.com"
)

@app.route('/')

def get_chunk():
    with open('app_status.txt') as f:
        status = f.read()
    status = status.rstrip()
    status = int(status)
    if status == 1:
        with open('app_status.txt', 'w+') as f:
            f.write(F'0')
        print('exiting')    
        die = requests.get('http://127.0.0.1:8080/shutdown')
        die
    if status == 0:
        #return get_chunk()
        pass

    # Using Tweepy, create an OAuthHandler instance, pass in a consumer key and secret,
    # then use an access token and secret to open the Twitter API.

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Open the html version of the ebook, then parse and clean it using BeautifulSoup.
    # The ebook used here is Thomas Frognall Dibdin's 1809 text about book collecting,
    # _Bibliomania; or Book Madness_. For discussion of Dibdin and his circle of
    # collectors, check out my book _The Queer Bookishness of Romanticism: Ornamental 
    # Community_.
    
    url = "http://www.gutenberg.org/files/28540/28540-h/28540-h.htm"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.decode()
    cleantext = BeautifulSoup(text, "html.parser").text.strip()

    # Slice a Twitter-appropriate length of text using the index from text_position.

    chunk_wrp = 'None'
    url = 'None'
    print('get_chunk attempted')
    got_chunk = False
    tag = ' #bibliomania1809'
    with open('text_position.txt') as f:
        index = f.read()
    index = index.rstrip()
    index = int(index)
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

    # For the next instance, update text_position with the endpoint of the slice.

    if got_chunk:
        new_index = index + 262
        update = False
        with open('text_position.txt', 'w+') as f:
            f.write(F'{new_index}')
            #f.close()
            update = True
        print('New index: ', new_index)

    # Send the current slice to Twitter.

    if update:
        print('attempting tweet')
        tweet = False
        try:
            #api.update_status('test')
            api.update_status(chunk_wrp)
            print('status updated')
            tweet = True
        except:
            print('Status update failed')

    # Create the app's weboutput by rendering an html template

    if tweet:
        with open('app_status.txt', 'w+') as f:
            f.write(F'1')
        die = requests.get('http://127.0.0.1:8080/shutdown')
        with app.app_context():
            return render_template('index.html', excrpt = chunk_wrp), die
            
@app.route('/shutdown', methods=['GET'])

def shutdown():
    print('Shutting down...')
    return os.kill(os.getpid(), signal.SIGINT)

if __name__ == '__main__':
    
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)
    

    #app.run(host='bibliomania.nn.r.appspot.com', port=8080, debug=True)
# [END gae_python38_render_template]


