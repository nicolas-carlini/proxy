from redis import Redis
import time

redis = Redis(host='redis', port=6379)


ip_limit = redis.mget(redis.keys('ip-limit-*'))
path_per_ip = redis.mget(redis.keys('path-per-ip-limit-*'))
print(ip_limit, path_per_ip)
