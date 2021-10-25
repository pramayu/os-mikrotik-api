import jwt
from functools import wraps
from flask import request, session
from api.modulefn.constants.jwtoken import decode_token, encode_payload
from api.modulefn.constants.respndfn import def_response
from uuid import uuid4


def secure_action(fn):
	@wraps(fn)

	def decorate(*args, **kwargs):
		response = def_response(topath='secure_action')
		response['tokenq'] = ''
		response['userlg'] = ''
		# get aks_token from cookie
		aks_token = request.cookies.get('aks_token')
		if len(aks_token) != 0 or aks_token != None:
			try:
				payload = decode_token(aks_token)
				uid = session[f'{payload["_id"]}']
				if payload and uid == payload['uid']:
					response['status'] = True
					response['messag'] = 'ok'
					response['userlg'] = payload['_id']
				else:
					response['messag'] = 'please re-login'
			except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
				ref_token = request.cookies.get('ref_token')
				if len(ref_token) != 0:
					try:
						payload = decode_token(ref_token)
						if payload and payload != None:
							session.pop(f'{payload["_id"]}',None)
							identity = uuid4().hex[:8]
							session[f'{payload["_id"]}'] = identity
							payload['uid'] = identity
							tokenq = encode_payload(payload, False)
							if tokenq != False:
								response['messag'] = 'ok'
								response['status'] = True
								response['tokenq'] = tokenq
								response['userlg'] = payload['_id']
							response['messag'] = 'please re-login'
						else:
							response['messag'] = 'please re-login'
					except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
						response['messag'] = 'please re-login'
				else:
					response['messag'] = 'please re-login'
		else:
			response['messag'] = 'please re-login'

		return fn(response, *args, **kwargs)
	return decorate