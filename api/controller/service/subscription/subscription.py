import graphene
from api.configure.middleware.secure_action import secure_action
from api.controller.schema.response import CommonRespd
from api.filemodel.db_payment import PaymentConfig

from api.routercmd.chrcmd.buildvpn import ConfigureVPN

class Subscription(graphene.Mutation):

	class Arguments:
		planprice 		= graphene.String()
		paymentyp 		= graphene.String()

	Output = CommonRespd
	
	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = PaymentConfig(response['userlg'])
			response = setup.besubscriber(
				kwargs['planprice'],
				kwargs['paymentyp'])
		else:
			response

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])

class PayoutOrder(graphene.Mutation):

	class Arguments:
		invoice 		= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = PaymentConfig(response['userlg'])
			response = setup.payoutorder(kwargs['invoice'])
		else:
			response

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])

class CancelOrder(graphene.Mutation):

	class Arguments:
		orderid 		= graphene.String()

	Output 	= CommonRespd

	@secure_action
	def mutate(response, root, info, **kwargs):

		if response['status'] == True:
			setup = PaymentConfig(response['userlg'])
			response = setup.cancelorder(kwargs['orderid'])
		else:
			response

		return CommonRespd(
			status=response['status'],
			messag=response['messag'],
			topath=response['topath'])