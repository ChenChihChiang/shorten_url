#!flask/bin/python
from flask import Flask, jsonify, redirect, abort, render_template, request, url_for
import string
import random
import redis
import codecs

app = Flask(__name__)

r = redis.Redis(
    host='redis-hk01.hyljtt.0001.apse1.cache.amazonaws.com',
    port=6379 
    )


def id_generator(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def get_shorten_url():
    
    shorten_url = id_generator()
    orginal_url = request.form.get('orginal_url')

    r.set(shorten_url, orginal_url)    

    return render_template('index.html', shorten_url=shorten_url, orginal_url=orginal_url)


@app.route('/<s_url>', methods=['GET'])
def url_mapping(s_url):

    url = r.get('%s' % s_url)
   
    o_url = url.decode()

    print (o_url)

    return redirect(o_url, code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
