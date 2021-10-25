import redis
connectredis = redis.Redis(host='127.0.0.1', port=6379, db=0)

def set_to_redis(key, value):
	try:
		connectredis.set(key, value)
		return True
	except Exception as e:
		return False

def get_from_redis(key):
	try:
		value = connectredis.get(key)
		return value
	except Exception as e:
		return False