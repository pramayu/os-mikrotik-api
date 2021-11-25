from api.controller.schema.routerconf_schema import RouterConfxRouterUserSchema
from api.controller.schema.routeraccount_schema import RouterAccountSchema
from api.controller.schema.routerint_schema import RouterInterfaceSchema
from api.filemodel.db import RouterUser, RouterConf, RouterInterface
from api.configure.middleware.connectclient import clientrouter
from api.modulefn.constants.respndfn import def_response
from api.modulefn.routercmd.liststring import to_string
from api.modulefn.hashedtxt.AEScipher import AESCipher
from api.modulefn.routercmd.ip_network import CalcIp
from api.filemodel.db import session, RouterAccount
from os import getenv

class RouterCommandLne(object):

	def __init__(self, routerapi):
		self.routerapi = routerapi
		self.errors = [False, None, {}, []]

	def encrypt_passwd(self, paswd):
		try:
			cipher = AESCipher(getenv('AESCIPHER'))
			cipher = cipher.encrypt(paswd)
			return cipher
		except Exception as e:
			return False

	def decrypt_passwd(self, hashd):
		try:
			cipher = AESCipher(getenv('AESCIPHER'))
			cipher = cipher.decrypt(hashd)
			return cipher
		except Exception as e:
			return False

	def get_index(self,obj,value,field):
		try:
			idx = list((idx) for idx, val in enumerate(obj) if val[field] == value)
			return idx
		except Exception as e:
			return False

	def get_serialnumber(self):
		try:
			# sn = self.routerapi.get_resource('/system/routerboard/')
			os = self.routerapi.get_resource('/system/resource').get()
			version = os[0]['version'].split('.')[:2]
			data = {
				'serialnumber': '558105',
				'osversion': '.'.join(version)
			}
			return data
		except Exception as e:
			return False

	def collect_user(self, api):
		try:
			fr = api.get_resource('/user').get()
			return fr
		except Exception as e:
			return False

	def collect_routeraccount(self, id):
		try:
			useradmin = session.query(RouterAccount).filter_by(id=id).first()
			schema = RouterAccountSchema()
			schema = schema.dump(useradmin)
			return schema
		except Exception as e:
			return False

	def collect_routerconf(self, id):
		try:
			routerconf = session.query(RouterConf).filter_by(id=id).first()
			schema = RouterConfxRouterUserSchema()
			schema = schema.dump(routerconf)
			return schema
		except Exception as e:
			return False

	def collect_routerint(self, name):
		try:
			routerint = session.query(RouterInterface).filter_by(name=name).first()
			schema = RouterInterfaceSchema()
			schema = schema.dump(routerint)
			return schema
		except Exception as e:
			return False

	def collect_basicnat(self,resp):
		try:
			fr = resp['rtrapi'].get_resource('/ip/firewall/nat/')\
			.get(comment='basic-nat-masquerade')
			return fr
		except Exception as e:
			return False

	def collect_bridge(self, bridge, resp):
		try:
			data = {}
			fr1 = resp['rtrapi'].get_resource('/interface/bridge/').get(name=bridge)
			fr2 = resp['rtrapi'].get_resource('/interface/bridge/port/').get(bridge=bridge)
			data['bridge'] = fr1 if fr1 else {}
			data['port'] = fr2 if fr2 else {}
			return data

		except Exception as e:
			return False

	def collect_interface(self, bridge, resp):
		try:
			fr = resp['rtrapi'].get_resource('/ip/address/').get()
			idx = self.get_index(fr,bridge,'interface')
			return idx
		except Exception as e:
			return False

	def collect_bridge_port(self, bridge, resp):
		try:
			fr = resp['rtrapi'].get_resource('/interface/bridge/port/').get()
			idx = self.get_index(fr,bridge,'bridge')
			return idx
		except Exception as e:
			return False

	def collect_bridge_idx(self,bridge,resp):
		try:
			fr = resp['rtrapi'].get_resource('/interface/bridge/').get()
			idx = self.get_index(fr,bridge,'name')
			return idx
		except Exception as e:
			return False

	@clientrouter
	def rename_router(resp, self, *args, **kwargs):
		response = def_response(topath='rename_router')

		if resp['status'] not in self.errors:
			try:
				rtrconf = self.collect_routerconf(resp['rtrcfg'])
				if rtrconf not in self.errors:
					fr = resp['rtrapi'].get_resource('/system/identity/')
					fr.set(name=args[0])
					session.query(RouterUser).\
					filter(RouterUser.id==rtrconf['routeruser']['id']).\
					update({RouterUser.routername: args[0]})
					session.commit()

					response['messag'] = 'ok'
					response['status'] = True
				else:
					response['messag'] = 'failed'
			except Exception as e:
				response['messag'] = 'something wrong'
		else:
			response['messag'] = resp['messag']

		return response

	@clientrouter
	def add_admin(resp, self, *args, **kwargs):
		response = def_response(topath='add_router_admin')
		if resp['status'] not in self.errors:

			user = self.collect_user(resp['rtrapi'])
			if list(filter(lambda x: x['name'] == args[0], user)):
				response['messag'] = 'use unique username'
			else:
				try:
					fr = resp['rtrapi'].get_resource('/user')
					fr.add(name=args[0],password=args[1],group=args[2])
					pswd = self.encrypt_passwd(args[1])

					user = RouterAccount(
						usernamert=args[0],
						privatekey=pswd,
						privilages=args[2],
						routerconfid=args[3])

					session.add(user)
					session.commit()
					response['status'] = True
					response['messag'] = 'ok'
				except Exception as e:
					response['messag'] = 'something wrong'
		else:
			response['messag'] = 'something wrong'

		return response

	@clientrouter
	def dtr_admin(resp, self, *args, **kwargs):
		response = def_response(topath='dtr_router_admin')
		if resp['status'] not in self.errors:
			try:
				user = self.collect_routeraccount(args[0])
				if user not in self.errors and user['usernamert'] != resp['cruser']:
					fr = resp['rtrapi'].get_resource('/user')
					fr.remove(id=user['usernamert'])
					session.query(RouterAccount).filter_by(id=args[0])\
					.delete(synchronize_session=False)
					session.commit()

					response['status'] = True
					response['messag'] = 'ok'
				else:
					response['messag'] = 'check user again'
			except Exception as e:
				response['messag'] = 'failed'
		else:
			response['messag'] = resp['messag']
		return response

	@clientrouter
	def port_address(resp, self, *args, **kwargs):
		response = def_response(topath='port_address')
		if resp['status'] not in self.errors:
			in_add = args[2].split('/')[0]
			ip_add = CalcIp(args[2])
			ip_add = ip_add.calc_ipaddres()
			if ip_add['network'] != in_add and ip_add['broadst'] != in_add:
				routerint = self.collect_routerint(args[1])
				if len(routerint) == 0:
					try:
						basicnatz = self.collect_basicnat(resp)
						routerint = RouterInterface(
							name=args[0],
							interface=args[1],
							ipaddress=args[2],
							submask=ip_add['submask'],
							routerconfid=resp['rtrcfg'])

						session.add(routerint)
						session.commit()

						# create bridge interface
						fr = resp['rtrapi'].get_resource('/interface/bridge/')
						fr.add(name=args[0],arp='enabled')
						# set port bridge
						fr = resp['rtrapi'].get_resource('/interface/bridge/port/')
						fr.add(interface=args[1],bridge=args[0])
						# set ip address to bridge interface
						fr = resp['rtrapi'].get_resource('/ip/address/')
						fr.add(
							address=args[2],
							interface=args[0],
							netmask=ip_add['submask'],
							network=ip_add['network'],
							broadcast=ip_add['broadst'])
						if len(basicnatz) == 0:
							fr = resp['rtrapi'].get_resource('/ip/firewall/nat/')
							fr.add(
								out_interface='INTERNET_ISP',
								action='masquerade',
								chain='srcnat',
								comment='basic-nat-masquerade')

						response['status'] = True
						response['messag'] = 'ok'

					except Exception as e:
						response['messag'] = 'something wrong'
				else:
					response['messag'] = 'use unique name'
			else:
				response['messag'] = 'combination ip addr & submask is invalid'
		else:
			response['messag'] = resp['messag']

		return response

	@clientrouter
	def upt_bridge_name(resp, self, *args, **kwargs):
		response = def_response(topath='upt_bridge_name')

		if resp['status'] not in self.errors:
			bridge = self.collect_bridge(args[0], resp)
			if len(bridge['bridge']) and len(bridge['port']) != 0:
				routerint = self.collect_routerint(args[0])
				if len(routerint) != 0:
					try:
						update = session.query(RouterInterface)\
						.filter(RouterInterface.name==args[0])\
						.update({
							RouterInterface.name : args[1] if args[1] != routerint['name'] else routerint['name'],
							RouterInterface.interface : args[2] if args[2] != routerint['interface'] else routerint['interface']
						})

						if bridge['bridge'][0]['name'] != args[1]:
							fr = resp['rtrapi'].get_resource('/interface/bridge/')
							fr.set(numbers=routerint['name'], name=args[1])

						if bridge['port'][0]['interface'] != args[2]:
							fr = resp['rtrapi'].get_resource('/interface/bridge/port/')
							fr.set(numbers=bridge['port'][0]['id'],interface=args[2])

						session.commit()
						response['status'] = True
						response['messag'] = 'ok'

					except Exception as e:
						response['messag'] = 'something wrong'
				else:
					response['messag'] = 'check interface'
			else:
				response['messag'] = 'check interface'
		else:
			response['messag'] = resp['messag']

		return response

	@clientrouter
	def delete_bridge_addr(resp, self, *args, **kwargs):
		response = def_response(topath='delete_bridge_addr')
		if resp['status'] == True:
			bridge = self.collect_bridge(args[0], resp)
			if bridge['bridge'] and bridge['port']:
				try:
					# delete address list
					addr = self.collect_interface(args[0], resp)
					fr = resp['rtrapi'].get_resource('/ip/address/')
					fr.remove(numbers=to_string(addr))
					# delete bridge port 
					port = self.collect_bridge_port(args[0], resp)
					fr = resp['rtrapi'].get_resource('/interface/bridge/port/')
					fr.remove(numbers=to_string(port))
					# delete bridge
					bridge_idx = self.collect_bridge_idx(args[0],resp)
					fr = resp['rtrapi'].get_resource('/interface/bridge/')
					fr.remove(numbers=to_string(bridge_idx))
					response['status'] = True
					response['messag'] = 'ok'
				except Exception as e:
					response['messag'] = 'check interface'
			else:
				response['messag'] = 'check interface'
		else:
			response['messag'] = resp['messag']

		return response
