import redis


def submit_node_testing(data):
    print(data)
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    red.hset(data[0], data[1], data[2])
