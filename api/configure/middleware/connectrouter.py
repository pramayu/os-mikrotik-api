import jwt
import routeros_api
from functools import wraps
from api.modulefn.constants.jwtoken import decode_token
from api.modulefn.constants.respndfn import def_response
from os import getenv

def connectrouter(validtoken):
	response = def_response(topath='connectrouter')
	response['api'] = ''
	try:
		if len(validtoken) != 0:
			payload = decode_token(validtoken)
			host = getenv('CHR_HOST').encode('utf-8')
			if (payload['transaction_status'] == 'settlement' 
				or payload['transaction_status'] == 'capture'):
				connect = routeros_api.RouterOsApiPool(
					host,username=getenv('CHR_SERVER'),
					password=getenv('CHR_KEY'),plaintext_login=True
				)
				api = connect.get_api()
				response['status'] 	= True
				response['messag'] 	= 'ok'
				response['api'] 	= api
			else:
				response['messag'] = 'something wrong'
		else:
			response['messag'] = 'invalid token'
	except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
		response['messag'] = 'invalid token'
	return response

