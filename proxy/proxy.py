import requests
from flask import Flask, redirect, url_for, request, Response
from redis import Redis
import os
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
s = requests.Session()
IP_LIMIT = int(os.environ.get('IP_LIMIT', 6000))
IP_LIMIT_PER_PATH = int(os.environ.get('IP_LIMIT_PER_PATH', 2000))
URL = os.environ.get('TARGET', 'https://api.mercadolibre.com')

@app.route('/')
def base():
    return Response(status=200)

@app.route('/<path:path>')
def proxy(path):
    redis_ip_limit = redis.incr(request.remote_addr)
    redis_path_per_ip = redis.incr(f'{request.remote_addr}-{path}')
    if redis_ip_limit <= IP_LIMIT and redis_path_per_ip <= IP_LIMIT_PER_PATH:
        response = requests.request(request.method, url=URL+'/'+path, headers=request.headers,params=request.form,  data=request.get_json(), allow_redirects=True)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.raw.headers.items() if name.lower() not in excluded_headers]
        return Response(response.content, response.status_code, headers)

    #return {'path':path,'method':request.method, 'headers': str(request.headers), 'request': request.method, 'ip': request.remote_addr, 'redis_ip_limit':redis_ip_limit, 'redis_path_per_ip':redis_path_per_ip}
    return Response(status=404)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

