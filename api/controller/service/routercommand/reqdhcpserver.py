import graphene
from api.configure.middleware.secure_action import secure_action
from api.routercmd.clientcmd.dhcpserver import RouterDHCPServer
from api.controller.schema.response import CommonRespd


class SetupAddrPool(graphene.Mutation):

	class Arguments:
		poolname 	= graphene.String()
		rangeadr	= graphene.String()
		nextpool	= graphene.String()


	Output 	= CommonRespd

	@secure_action
	def mutate(response, info, root, **kwargs):
		if response['status'] == True:
			setup = RouterDHCPServer(None)
			response = setup.ip_pool(
				kwargs['poolname'],
				kwargs['rangeadr'],
				kwargs['nextpool']
				)
		else:
			response['topath'] = 'set_ip_pool'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])


class SetupDHCPServer(graphene.Mutation):

	class Arguments:
		ethernet 	= graphene.String()
		pooladdr 	= graphene.String()
		dhcpname 	= graphene.String()
		dnserver 	= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):
		if response['status'] == True:
			setup = RouterDHCPServer(None)
			response = setup.set_dhcpserver(
				kwargs['ethernet'],
				kwargs['pooladdr'],
				kwargs['dhcpname'],
				kwargs['dnserver'])
		else:
			response['topath'] = 'dhcp_server_setup'

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])