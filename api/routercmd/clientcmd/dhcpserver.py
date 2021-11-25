from api.configure.middleware.connectclient import clientrouter
from api.modulefn.constants.respndfn import def_response
from api.modulefn.routercmd.liststring import to_string
from api.filemodel.db import session, RouterAccount

class RouterDHCPServer(object):

	def __init__(self):
		self.errors = [False, None, {}, []]

	def get_bridges(self,api):
		try:
			fr = api.get_resource('interface/bridge').get()
			return fr
		except Exception as e:
			return "Bridge not found!"

	def get_bridgeport(self, api):
		try:
			fr = api.get_resource('interface/bridge/port').get()
			return fr
		except Exception as e:
			return "Port no found!"

	def get_ip_pool(self, name, api):
		try:
			fr = api.get_resource('ip/pool')\
			.get(name=name)
			return fr
		except Exception as e:
			return False

	def get_bridgename(self, ether, api):
		try:
			fr = api.get_resource('ip/address')\
			.get(interface=ether)
			return fr
		except Exception as e:
			return False

	@clientrouter
	def ip_pool(rtrapi, self, *args, **kwargs):
		response = def_response(topath='set_ip_pool')
		if rtrapi['status'] == True:
			try:
				pool = self.get_ip_pool(args[0], api)
				if pool:
					response['messag'] = 'Use Unique Pool Name'
				else:
					fr = rtrapi['api'].get_resource('ip/pool')
					if nextpool:
						fr.add(name=args[0], ranges=args[1], next_pool=args[2])
					else:
						fr.add(name=args[0], ranges=args[1])

			except Exception as e:
				response['messag'] = 'Something Wrong'
		else:
			response['messag'] = rtrapi['messag']

		return response


	def set_network(self, ether, dns, api):
		try:
			netwrk = self.get_bridgename(ether, api)
			if netwrk:
				gw = netwrk['address'].split('/')
				nw = f"{netwrk['network']}/{gw[1]}"
				fr = api.get_resource('ip/dhcp-server/network')
				fr.add(
					address=netwrk['network'],
					gateway=gw[0],
					dns_server=dns
					)
			else:
				return 'Something Wrong'
		except Exception as e:
			return False

	def set_dhcpsnoop(self, ether, api):
		try:
			bridge = self.get_bridges(api)
			if bridge:
				index = list(idx for (idx, val) in enumerate(bridge) if val['name'] == ether)
				fr = api.get_resource('interface/bridge')
				fr.set(numbers=str(index[0]), dhcp_snooping='yes')
			else:
				return bridge
		except Exception as e:
			return False

	def set_trustedport(self, ether, api):
		bridgeport = self.get_bridgeport(api)
		try:
			if bridgeport:
				index = list(idx for (idx, val) in enumerate(bridge) if val['bridge'] == ether)
				fr = api.get_resource('interface/bridge/port')
				fr.set(numbers=to_string(index), trusted='yes')
			else:
				return bridgeport
		except Exception as e:
			return False

	@clientrouter
	def set_dhcpserver(rtrapi, self, *args, **kwargs):
		response = def_response(topath='set_dhcp_server')
		if rtrapi['status'] == True:
			try:
				self.set_network(args[0], args[3], rtrapi['api'])

				fr = api.get_resource('ip/dhcp-server')
				fr.add(name=name,address_pool=pool,
					interface=ether,disabled='no')

				self.set_dhcpsnoop(args[0],rtrapi['api'])
				self.set_trustedport(args[0],rtrapi['api'])
			except Exception as e:
				response['messag'] = 'something wrong'
		else:
			response['messag'] = rtrapi['messag']

		return response