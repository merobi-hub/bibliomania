import datetime
import time
from flask import Flask, render_template, request, jsonify
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import textwrap
from static.hidden import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
from tweepy import TweepError
import sys
import requests
import signal
import os
from google.cloud import storage

app = Flask(__name__, template_folder = 'templates')
app.config.update(
    SERVER_NAME = "127.0.0.1:8080"
    #SERVER_NAME = "bibliomania.nn.r.appspot.com"
)

@app.route('/', methods=['GET'])

def get_chunk():

    # Download endpoint from last execution from blob in G Cloud Storage bucket

    try:
        # Delete CLOUD_BUCKET variable definition before production (belongs in app.yaml)
        CLOUD_BUCKET = "bibliomania.appspot.com"        
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(CLOUD_BUCKET)
        blob = bucket.get_blob('text_position.txt')
        new_index = blob.download_as_bytes()
        index = str(new_index)        
        index = int(new_index)
        print('downloaded index:', index)
    except:
        print('index download failed')
         
    # Open the html or txt version of the ebook, then parse and clean it using 
    # BeautifulSoup. The ebook used here is Thomas Frognall Dibdin's 1809 text about 
    # book collecting,_Bibliomania; or Book Madness_. For discussion of Dibdin and his 
    # circle of collectors, check out my book _The Queer Bookishness of Romanticism: 
    # Ornamental Community_.

    # To access the html version of the ebook:

    #url = "http://www.gutenberg.org/files/28540/28540-h/28540-h.htm"
    #html = urlopen(url).read()
    #soup = BeautifulSoup(html, "html.parser")
    #text = soup.decode()
    #cleantext = BeautifulSoup(text, "html.parser").text.strip()

    # To access the local txt version of the ebook:

    with open('static/Dibdin_Bibliomania.txt', errors='ignore') as f:
        cleantext = f.read()
    cleantext = cleantext.rstrip()

    # Slice a Twitter-appropriate length of text (ending with a punctuation mark if 
    # possible) using the index from text_position.txt.

    wrapper = textwrap.TextWrapper(width = 30, expand_tabs = False, replace_whitespace = True, drop_whitespace = True)
    chunk_wrp = 'None'
    got_chunk = False
    tag = ' #bibliomania1809'
    big_chunk = cleantext[index:index + 262]
    term = big_chunk.rfind('.')
    chunk = big_chunk[0:term + 1]
    
    if chunk[term - 2:term] == 'Mr':
        term = term - 1
        term = chunk.rfind('.', 0, term)
        chunk = chunk[0:term + 1]

    if chunk[term - 2:term] == 'MR':
        term = term - 1
        term = chunk.rfind('.', 0, term)
        chunk = chunk[0:term + 1]

    if chunk[term - 2:term] == 'Dr':
        term = term - 1
        term = chunk.rfind('.', 0, term)
        chunk = chunk[0:term + 1]

    if chunk[term - 2:term] == 'DR':
        term = term - 1
        term = chunk.rfind('.', 0, term)
        chunk = chunk[0:term + 1]
    check = term + 1

    try:
        if check <= len(big_chunk):
            if big_chunk[term + 1] == '"':
                term = term + 1
                chunk = big_chunk[0:term + 1]
    except:
        pass
    
    if len(chunk) != 0:
        tagged_chunk = chunk + tag
        new_index = index + len(chunk)

    if len(chunk) == 0:
        chunk = cleantext[index:index + 262]
        term = chunk.rfind('!')

        try:
            if chunk[term + 1] <= len(chunk):
                if chunk[term + 1] == '"':
                    term = term + 1
        except:
            pass

        chunk = chunk[0:term + 1]
        
        if len(chunk) != 0:
            tagged_chunk = chunk + tag
            new_index = index + len(chunk)

        else:
            chunk = cleantext[index:index + 262]
            term = chunk.rfind('?')

            try:
                if chunk[term + 1] <= len(chunk):
                    if chunk[term] == '"':
                        term = term + 1
            except:
                pass

            chunk = chunk[0:term + 1]
            
            if len(chunk) != 0:
                tagged_chunk = chunk + tag
                new_index = index + len(chunk)

            else:
                chunk = cleantext[index:index + 262]
                term = chunk.rfind(';')

                try:
                    if chunk[term + 1] <= len(chunk):
                        if chunk[term + 1] == '"':
                            term = term + 1
                except:
                    pass

                chunk = chunk[0:term + 1]
                
                if len(chunk) != 0:
                    tagged_chunk = chunk + tag
                    new_index = index + len(chunk)
                   
                else:
                    chunk = cleantext[index:index + 262]
                    term = chunk.rfind(':')

                    try:
                        if chunk[term + 1] <= len(chunk):
                            if chunk[term + 1] == '"':
                                term = term + 1
                    except:
                        pass

                    chunk = chunk[0:term + 1]
                    
                    if len(chunk) != 0:
                        tagged_chunk = chunk + tag
                        new_index = index + len(chunk)
                        
                    else:
                        chunk = cleantext[index:index + 262]
                        term = chunk.rfind(',')

                        try:
                            if chunk[term + 1] <= len(chunk):
                                if chunk[term] == '"':
                                    term = term + 1
                        except:
                            pass

                        chunk = chunk[0:term + 1]
                        
                        if len(chunk) != 0:
                            tagged_chunk = chunk + tag
                            new_index = index + len(chunk)
                            
                        else:
                            chunk = cleantext[index:index + 262]
                            tagged_chunk = chunk + tag
                            new_index = index + 262
                            print(new_index) 
                        
    tagged_chunk = textwrap.dedent(tagged_chunk).strip()
    tagged_chunk = wrapper.fill(tagged_chunk)
    print('tagged_chunk:', tagged_chunk)
    got_chunk = True
    
    # Send the chunk to twitter.

    if got_chunk:

        print('Attempting tweet')
        tweet = False
        try:
            
            # Using Tweepy, create an OAuthHandler instance, pass in a consumer key and secret,
            # then use an access token and secret to open the Twitter API.

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            #api.update_status('test')
            api.update_status(tagged_chunk)
            print('Status updated')
            tweet = True
            
        except:
            print('Status update failed')

    # Upload the time of tweet for the weboutput function

    if tweet:
        update_tweettime = False
        now = datetime.datetime.now()
        tweettime = now.strftime("%Y-%m-%d %H:%M:%S")
        print('tweettime for upload:', tweettime)
        destination_blob_name = 'tweettime.txt'
        storage_client = storage.Client()
        bucket = storage_client.bucket(CLOUD_BUCKET)
        blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(tweettime)
        update_tweettime = True
        print('tweettime upload OK')
    except:
        print('tweettime upload failed')

    # For the next instance, update a blob in G Cloud Storage bucket with the endpoint of the slice.

    if update_tweettime:

        update_index = False
        new_index = str(new_index)        
        destination_blob_name = 'text_position.txt'
        storage_client = storage.Client()
        bucket = storage_client.bucket(CLOUD_BUCKET)
        blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(new_index)
        update_index = True
        print('index upload OK')
    except:
        print('index upload failed')

    # Update a different blob with the current chunk.

    if update_index:

        update_chunk = False        
        destination_blob_name = 'chunk_wrp.txt'
        storage_client = storage.Client()
        bucket = storage_client.bucket(CLOUD_BUCKET)
        blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(tagged_chunk)
        update_chunk = True
        print('chunk upload OK')
    except:
        print('upload of chunk failed')

    if update_chunk:
        shutdown_page = ['http://127.0.0.1:8080/shutdown']
        for url in shutdown_page:
            die = requests.get(url)
        return die

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


