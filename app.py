#!flask/bin/python
from flask import Flask, jsonify, redirect, abort, render_template, request, url_for
import string
import random
import redis
import codecs

app = Flask(__name__)

#建立 redis 連線
r = redis.Redis(
    host='redis-hk01.hyljtt.0001.apse1.cache.amazonaws.com',
    port=6379 
    )


#建立八碼短網址字串
def id_generator(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
def index():

    #一開始先導到首頁
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def get_shorten_url():

    #取得短網址   
    shorten_url = id_generator()
    #從網頁取得原始網址
    orginal_url = request.form.get('orginal_url')
    #存入 redis
    r.set(shorten_url, orginal_url)    
    #回傳結果
    return render_template('index.html', shorten_url=shorten_url, orginal_url=orginal_url)

#轉址功能
@app.route('/<s_url>', methods=['GET'])
def url_mapping(s_url):

    #如果輸入的網址不是空值，就在 redis 中找出對應的值，如果是就導回首頁
    if s_url:

        url = r.get('%s' % s_url)
   
        o_url = url.decode()

        return redirect(o_url, code=301)
    
    else:
            
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,threaded=True,debug=True)
