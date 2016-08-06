import redis
redis = redis.StrictRedis(host='123.206.211.77',
                          port='6379', db=0, password='abc@123')


def castrocket(data):
    if data:
        redis.publish('rocketinfo', data)
