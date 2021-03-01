from flask import Flask, render_template
import datetime
from google.cloud import storage

app = Flask(__name__, template_folder = 'templates')
#app.config.update(
#    SERVER_NAME = "127.0.0.1:8080"
    #SERVER_NAME = "bibliomania.nn.r.appspot.com"
#)
    
@app.route('/')

def weboutput():
    
    # Delete CLOUD_BUCKET variable definition before production (belongs in app.yaml)
    CLOUD_BUCKET = "bibliomania.appspot.com"        
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_BUCKET)
    try:
        blob = bucket.get_blob('tweettime.txt')
        tweettime = blob.download_as_bytes()
        tweettime = tweettime.decode('utf-8')
        print('downloaded tweettime for webpage:', tweettime)
    except:
        pass

    blob = bucket.get_blob('text_position.txt')
    new_index = blob.download_as_bytes()
    index = str(new_index)
    index = int(new_index)
    print('downloaded index for webpage:', index)

    blob = bucket.get_blob('chunk_wrp.txt')
    chunk_wrp = blob.download_as_bytes()
    str_chunk_wrp = chunk_wrp.decode()
    #str_chunk_wrp = str(chunk_wrp)
    print('chunk for webpage:', str_chunk_wrp)

    with app.app_context():
        return render_template('index.html', excrpt = str_chunk_wrp, new_index = index, tweettime = tweettime)
        
if __name__ == '__main__':
    
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.

    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=True)
    #app.run(host='bibliomania.nn.r.appspot.com', port=8080, debug=True)    