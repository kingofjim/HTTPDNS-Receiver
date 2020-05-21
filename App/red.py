import redis


def submit_node_testing(data):
    print(data)
    red = redis.StrictRedis(host='172.17.2.6', port=6379, db=0, password='last1mile')
    red.hset(data[0], data[1], data[2])
