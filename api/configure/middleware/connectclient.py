import routeros_api, json
from functools import wraps
from api.modulefn.constants.respndfn import def_response
from api.configure.middleware.connectredis import get_from_redis
from api.modulefn.hashedtxt.AEScipher import AESCipher
from api.modulefn.constants.jwtoken import decode_token
from os import getenv
from flask import request

errors = [False, None, [], {}]

def extract_passwd(hashed):
	try:
		setup = AESCipher(getenv('AESCIPHER'))
		plain = setup.decrypt(hashed)
		return plain
	except Exception as e:
		return False

def routerapi(ip, port, username, password, osversion):
	plaintext = extract_passwd(password)
	if plaintext not in errors:
		try:
			if osversion < 6.43:
				connection = routeros_api.RouterOsApiPool(
					ip, username=username, password=plaintext, port=int(port),
					use_ssl=False,)
			if osversion >= 6.43:
				connection = routeros_api.RouterOsApiPool(
					ip, username=username, password=plaintext,
					port=int(port),plaintext_login=True,use_ssl=False,)
			api = connection.get_api()
			return api
		except Exception as e:
			return False
	else:
		return False


def clientrouter(fn):
	@wraps(fn)

	def decorate(*args, **kwargs):
		reserror = [False, None, {}, []]
		response = def_response(topath='connectclientrouter')
		response['rtrapi'] = None
		response['cruser'] = ''
		response['rtrcfg'] = ''

		def get_cookie():
			try:
				rtrid = request.cookies.get('rtrid')
				payld = decode_token(rtrid)
				return payld
			except Exception as e:
				return False

		payload = get_cookie()
		if payload not in reserror:
			key = f"{payload['_id']}_{payload['user']}"
			val = get_from_redis(key);val=json.loads(val)
			if val not in reserror:
				api = routerapi(
					val['ipaddress'],val['userports'],
					val['username'],val['password'],
					float(val['osversion']))
				if api not in reserror:
					response['status'] = True
					response['messag'] = 'ok'
					response['cruser'] = val['username']
					response['rtrapi'] = api
					response['rtrcfg'] = payload['_id']
				else:
					response['messag'] = 'failed'
			else:
				response['messag'] = 'failed'
		else:
			response['messag'] = 'failed or re-login'

		return fn(response, *args, **kwargs)
	return decorate


# redis.exists