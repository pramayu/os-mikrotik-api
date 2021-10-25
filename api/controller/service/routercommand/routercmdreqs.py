import graphene
from api.configure.middleware.secure_action import secure_action
from api.routercmd.clientcmd.clientcmd import RouterCommandLne
from api.controller.schema.response import CommonRespd

class RenameRouterId(graphene.Mutation):

	class Arguments:
		routername	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):
		if response['status'] == True:
			setup = RouterCommandLne(None)
			response = setup.rename_router(
				kwargs['routername'])
		else:
			response['topath'] = 'rename_routerid'
			
		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])

class AddRouterAdmin(graphene.Mutation):

	class Arguments:
		username 	= graphene.String()
		password 	= graphene.String()
		privilag 	= graphene.String()
		routrcfg	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):
		if response['status'] == True:
			setup = RouterCommandLne(None)
			response = setup.add_admin(
				kwargs['username'],
				kwargs['password'],
				kwargs['privilag'],
				kwargs['routrcfg'])
		else:
			response['topath'] = 'add_router_admin'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])


class DtrRouterAdmin(graphene.Mutation):

	class Arguments:
		routeradmin 	= graphene.String()

	Output = CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):
		if response['status'] == True:
			setup = RouterCommandLne(None)
			response = setup.dtr_admin(
				kwargs['routeradmin'])
		else:
			response['topath'] = 'dtr_router_admin'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])

class PortAddressing(graphene.Mutation):

	class Arguments:
		bridgename		= graphene.String()
		interfaces 		= graphene.String()
		ipaddreses		= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = RouterCommandLne(None)
			response = setup.port_address(
				kwargs['bridgename'],
				kwargs['interfaces'],
				kwargs['ipaddreses'])
		else:
			response['path'] = 'port_address'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])


class UptBridgeNamez(graphene.Mutation):

	class Arguments:
		bridgenam1 	= graphene.String()
		bridgenam2 	= graphene.String()
		interfaces 	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = RouterCommandLne(None)
			response = setup.upt_bridge_name(
				kwargs['bridgenam1'],
				kwargs['bridgenam2'],
				kwargs['interfaces'])
		else:
			response['path'] = 'upt_bridge_name'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])