import graphene
from api.controller.service.useraccount.signup import UserSignUp
from api.controller.service.useraccount.signup import ActivateUser
from api.controller.service.useraccount.signin import UserSignIn
from api.controller.service.useraccount.verify import UserVerify

# be subscriber
from api.controller.service.subscription.subscription import Subscription
from api.controller.service.subscription.subscription import PayoutOrder
from api.controller.service.subscription.subscription import CancelOrder

# routerconf
from api.controller.service.routerconfig.routersetting import BuildRouterConf
from api.controller.service.routerconfig.routersetting import UpdateRouterConf
from api.controller.service.routerconfig.routersetting import StoreRouterUser
from api.controller.service.routerconfig.routersetting import UpdateRouterUser

# routerconnect
from api.controller.service.routerconfig.routerconnect import ConnectRouterClient

'''
router client
command here
'''
from api.controller.service.routercommand.routercmdreqs import RenameRouterId
from api.controller.service.routercommand.routercmdreqs import AddRouterAdmin
from api.controller.service.routercommand.routercmdreqs import DtrRouterAdmin
from api.controller.service.routercommand.routercmdreqs import PortAddressing
from api.controller.service.routercommand.routercmdreqs import UptBridgeNamez
from api.controller.service.routercommand.routercmdreqs import DestBridgeAddr

'''
setup dhcp server
'''
from api.controller.service.routercommand.reqdhcpserver import SetupAddrPool
from api.controller.service.routercommand.reqdhcpserver import SetupDHCPServer


class MainService(graphene.ObjectType):
	usersignup 			= UserSignUp.Field()
	activeuser 			= ActivateUser.Field()
	usersignin 			= UserSignIn.Field()
	userverify 			= UserVerify.Field()

	subscribe  			= Subscription.Field()
	payoutorder 		= PayoutOrder.Field()
	cancelorder 		= CancelOrder.Field()

	buildrouterconf 	= BuildRouterConf.Field()
	updaterouterconf 	= UpdateRouterConf.Field()
	storerouteruser 	= StoreRouterUser.Field()
	updaterouteruser 	= UpdateRouterUser.Field()

	connectclient 		= ConnectRouterClient.Field()

	addrouteradmin 		= AddRouterAdmin.Field()
	dtrrouteradmin 		= DtrRouterAdmin.Field()
	renamerouterid 		= RenameRouterId.Field()
	portaddressing 		= PortAddressing.Field()
	updtbridgename 		= UptBridgeNamez.Field()
	destbridgeaddr 		= DestBridgeAddr.Field()

	setupaddrpool 		= SetupAddrPool.Field()
	setupdhcpserver 	= SetupDHCPServer.Field()
