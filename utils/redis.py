import redis
import os

# 连接redis池
redis_conn = redis.ConnectionPool(host="47.98.113.173",port=6379, password=os.environ.get("TestRedis"), db=7)
my_redis = redis.Redis(connection_pool=redis_conn)

#在redis中添加信息
def setRedis(db, key, result):
    redis_res = my_redis.hset(db, key , result)
    return redis_res
