import graphene
from api.controller.schema.response import CommonRespd, TokenRespd
from api.filemodel.db_user import UserConfig
from api.modulefn.constants.respndfn import def_response
from api.configure.middleware.verify_token import accesstoken
from flask import make_response


class UserVerify(graphene.Mutation):

	Output 	= TokenRespd

	@accesstoken
	def mutate(response, root, info, **kwargs):
		
		if response['status'] == True and response['topath'] == 'accesstoken':
			response
		else:
			response['topath'] = 'user_verify'

		return TokenRespd(tokenq=response['tokenq'], common=response)