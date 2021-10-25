from functools import wraps
import re
from api.modulefn.constants.respndfn import def_response


def signupmethod(fn):
	@wraps(fn)

	def decorate(*args, **kwargs):
		response = def_response(topath='inputmethod')
		strcheck = re.compile('[@!#$%^&*()<>?/\|}{~:]')
		try:
			username = kwargs['username']
			password = kwargs['password']
			phonenum = kwargs['phonenum']

			if len(username.split(" ")) == 1 and strcheck.search(username) == None:
				if len(password) >= 8:
					if phonenum.isdecimal():
						response['status'] = True
						response['messag'] = 'ok'
					else:
						response['messag'] = 'check phone'
				else:
					response['messag'] = 'password length 8 or more'
			else:
				response['messag'] = 'please check username!'

		except Exception as e:
			response['messag'] = 'something wrong!'

		return fn(response, *args, **kwargs)
	return decorate

def signinmethod(fn):
	@wraps(fn)

	def decorate(*args, **kwargs):
		response = def_response(topath='signinmethod')

		if len(kwargs['identity']) != 0:
			if len(kwargs['password']) >= 8:
				response['status'] = True
				response['messag'] = 'ok'
			else:
				response['messag'] = 'check password'
		else:
			response['messag'] = 'check identity'

		return fn(response, *args, **kwargs)

	return decorate