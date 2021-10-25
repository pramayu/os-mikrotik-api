import graphene
from api.configure.middleware.secure_action import secure_action
from api.controller.schema.response import TokenRespd
from api.filemodel.db_router import RouterConfig


class ConnectRouterClient(graphene.Mutation):

	class Arguments:
		username 		= graphene.String()
		password 		= graphene.String()
		ipaddres 		= graphene.String()
		userport		= graphene.String()
		rtrcnfid 		= graphene.String()

	Output 	= TokenRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = RouterConfig(response['userlg'],None)
			response = setup.connect_router_client(
				kwargs['username'],
				kwargs['password'],
				kwargs['ipaddres'],
				kwargs['userport'],
				kwargs['rtrcnfid'])
		else:
			response['topath'] = 'connect_router_client'

		return TokenRespd(
			tokenq=response['tokenq'],
			common=response)