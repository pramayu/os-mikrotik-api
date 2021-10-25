from api.modulefn.constants.respndfn import def_response
from api.modulefn.hashedtxt.encrypt import bcrypt_en
from api.modulefn.hashedtxt.decrypt import bcrypt_de
from api.controller.schema.user_schema import UserSchema
from api.filemodel.db import session, User
from api.modulefn.constants.jwtoken import encode_payload
from sqlalchemy import or_
from uuid import uuid4


class UserConfig(object):

	def __init__(self, username):
		self.username 	= username
		
	def find_by_username(self):
		try:
			user = session.query(User).filter_by(username=self.username).first()
			return user
		except Exception as e:
			return False

	def find_by_indentity(self, identity):
		try:
			user = session.query(User)\
			.filter(or_(User.username == identity, User.phonenum == identity)).first()
			return user
		except Exception as e:
			return False

	def find_by_otp(self, otpdigit):
		try:
			user = session.query(User).filter_by(otpdigit=otpdigit).first()
			return user
		except Exception as e:
			return False

	def insert_user(self, password, phonenum):

		response = def_response(topath='signup_user')

		try:
			checkuser = self.find_by_username()
			print(checkuser)
			if checkuser == None and checkuser != False:
				hashed = bcrypt_en(password)
				digits = uuid4().hex[:6].upper()
				# # insert new user
				userad = User(username=self.username, otpdigit=digits,
				password=hashed, phonenum=phonenum)
				session.add(userad)
				session.commit()

				response['messag'] = 'ok'
				response['status'] = True
			else:
				response['messag'] = 'username has taken.'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong.'

		return response

	def active_user(self, digitotp):
		response = def_response(topath='activate_user')
		response['tokenq'] = ''
		response['_id'] = ''

		try:
			checkuser = self.find_by_otp(digitotp)
			if checkuser != None and checkuser != False:
				digits = uuid4().hex[:6].upper()

				# get user data
				user_schema = UserSchema()
				data = user_schema.dump(checkuser)
				# create refresh token
				data1 = {
					'_id': data['id'],
					'nickname': data['username']
				}
				token= encode_payload(data1, True)
				if len(token) != 0 and data['activate'] == False:
					session.query(User).filter(User.otpdigit==digitotp)\
					.update({User.activate: True, User.otpdigit: digits})
					session.commit()
				
					response['messag'] 	= 'ok'
					response['status'] 	= True
					response['tokenq'] 	= token
				else:
					response['messag'] = 'something wrong.'				
			else:
				response['messag'] = 'user not found!'
		except Exception as e:
			response['messag'] = 'something wrong.'

		return response

	def check_login(self, identity, password):

		response = def_response(topath='signin_user')
		response['tokenq'] = ''

		try:
			user = self.find_by_indentity(identity)
			user_schema = UserSchema()
			data = user_schema.dump(user)
			resp = bcrypt_de(password, data['password'])
			if resp == True:
				data1 = {
					'_id': data['id'],
					'nickname': data['username']
				}
				token= encode_payload(data1, True)
				response['messag'] = 'ok'
				response['status'] = True
				response['tokenq'] = token
			else:
				response['messag'] = 'check identity or password'
		except Exception as e:
			response['messag'] = 'something wrong'

		return response