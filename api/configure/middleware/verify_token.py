import jwt
from functools import wraps
from flask import request, session
from api.modulefn.constants.respndfn import def_response
from api.modulefn.constants.jwtoken import decode_token, encode_payload
from uuid import uuid4

def accesstoken(fn):
	@wraps(fn)

	def decorate(*args, **kwargs):
		response = def_response(topath='accesstoken')
		response['tokenq'] = ''

		# refresh token from cookies
		cookies_ref = request.cookies.get('ref_token')

		if cookies_ref:
			try:
				payload = decode_token(cookies_ref)
				if len(payload) != 0:
					session.pop(f'{payload["_id"]}',None)
					identity = uuid4().hex[:8]
					session[f'{payload["_id"]}'] = identity
					payload['uid'] = identity
					tokenq = encode_payload(payload, False)
					response['status'] = True
					response['messag'] = 'ok'
					response['tokenq'] = tokenq
				else:
					response['messag'] = 'something wrong'
			except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
				response['messag'] = 'please re-login'
		else:
			response['messag'] = 'please re-login'
		
		return fn(response, *args, **kwargs)
	return decorate

