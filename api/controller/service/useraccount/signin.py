import graphene
from api.controller.schema.response import TokenRespd
from api.configure.middleware.inputmethod import signinmethod
from api.filemodel.db_user import UserConfig
from api.modulefn.constants.respndfn import def_response


class UserSignIn(graphene.Mutation):

	class Arguments:
		identity 		= graphene.String()
		password 		= graphene.String()

	Output 	= TokenRespd


	@signinmethod
	def mutate(response, root, info, **kwargs):
		response['tokenq'] = ''
		if response['status'] == True and response['topath'] == 'signinmethod':
			setup = UserConfig(None)
			response = setup.check_login(kwargs['identity'],kwargs['password'])
		else:
			response

		return TokenRespd(tokenq=response['tokenq'], common=response)
