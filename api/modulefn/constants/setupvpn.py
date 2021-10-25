from api.configure.middleware.connectrouter import connectrouter
from api.routercmd.chrcmd.buildvpn import ConfigureVPN



def configurevpn(payload, validtoken):
	try:
		respd = connectrouter(validtoken)
		setup = ConfigureVPN(respd['api'])
		setup.buildvpnschedule(payload['invoiceid'])
	except Exception as e:
		return False