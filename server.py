import requests
from flask import Flask, redirect, url_for, request
from redis import Redis
import os
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
s = requests.Session()
IP_LIMIT = os.environ.get('ip_limit')

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

@app.route('/p/<path:path>')
def proxy(path):
    redis_ip_limit = redis.incr(request.remote_addr)
    redis_path_per_ip = redis.incr(f'{request.remote_addr}-{path}')
    request
    return {'path':path,'method':request.method, 'headers': str(request.headers), 'request': request.method, 'ip': request.remote_addr, 'redis_ip_limit':redis_ip_limit, 'redis_path_per_ip':redis_path_per_ip}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)