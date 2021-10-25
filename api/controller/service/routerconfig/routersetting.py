import graphene
from api.configure.middleware.secure_action import secure_action
from api.controller.schema.response import CommonRespd
from api.filemodel.db_router import RouterConfig



class BuildRouterConf(graphene.Mutation):

	class Arguments:
		serialnumb 		= graphene.String()
		routerosve		= graphene.String()
		routeruserid	= graphene.String()
		ispbandwidth 	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = RouterConfig(response['userlg'], None)
			response = setup.build_router_conf(
				kwargs['serialnumb'],
				kwargs['routerosve'],
				kwargs['routeruserid'],
				kwargs['ispbandwidth'])
		else:
			response['topath'] = 'build_router_conf'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])


class UpdateRouterConf(graphene.Mutation):

	class Arguments:
		routerconfid 	= graphene.String()
		serialnumb 		= graphene.String()
		routerosve		= graphene.String()
		routeruserid	= graphene.String()
		ispbandwidth 	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):
		if response['status'] == True:
			setup = RouterConfig(response['userlg'], None)
			response = setup.update_router_conf(
				kwargs['routerconfid'],
				kwargs['serialnumb'],
				kwargs['routerosve'],
				kwargs['routeruserid'],
				kwargs['ispbandwidth'])
		else:
			response['messag'] = 'update_router_conf'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])


class StoreRouterUser(graphene.Mutation):

	class Arguments:
		usernamert 		= graphene.String()
		privatekey 		= graphene.String()
		privilage 		= graphene.String()
		routerconfid 	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):
		if response['status'] == True:
			setup = RouterConfig(response['userlg'], None)
			response = setup.store_router_account(
				kwargs['usernamert'],
				kwargs['privatekey'],
				kwargs['privilage'],
				kwargs['routerconfid'])
		else:
			response['topath'] = 'store_router_user'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])

class UpdateRouterUser(graphene.Mutation):

	class Arguments:
		routeraccid 	= graphene.String()
		usernamert 		= graphene.String()
		privatekey 		= graphene.String()
		privilage 		= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = RouterConfig(response['userlg'], None)
			response = setup.update_ruoter_account(
				kwargs['routeraccid'],
				kwargs['usernamert'],
				kwargs['privatekey'],
				kwargs['privilage'])
		else:
			response['topath'] = 'update_ruoter_account'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])