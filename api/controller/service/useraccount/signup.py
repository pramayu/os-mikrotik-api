import graphene
from api.controller.schema.response import CommonRespd, TokenRespd
from api.configure.middleware.inputmethod import signupmethod
from api.filemodel.db_user import UserConfig
from api.modulefn.constants.respndfn import def_response
from flask import session
from uuid import uuid4

class UserSignUp(graphene.Mutation):

	class Arguments:
		username 	= graphene.String()
		phonenum	= graphene.String()
		password 	= graphene.String()

	Output  = CommonRespd

	@signupmethod
	def mutate(response, root, info, **kwargs):

		if response['status'] == True and response['topath'] == 'inputmethod':
			setup = UserConfig(kwargs['username'])
			response = setup.insert_user(
				kwargs['password'],
				kwargs['phonenum'])
		else:
			response['topath'] = 'signup_user'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])


class ActivateUser(graphene.Mutation):

	class Arguments:
		digitotp		= graphene.String()

	Output 	= TokenRespd


	def mutate(root, info, **kwargs):

		response = def_response(topath='activate_user')
		response['tokenq'] = ''

		if len(kwargs['digitotp']) != 0:
			setup = UserConfig(None)
			response = setup.active_user(kwargs['digitotp'])
		else:
			response['messag'] = 'please check pin'

		return TokenRespd(
			common=response,
			tokenq=response['tokenq'])