from api.filemodel.db import session, RouterUser, RouterConf, RouterAccount
from api.controller.schema.routeraccount_schema import RouterAccountSchema
from api.controller.schema.routeruser_schema import RouterUserSchema
from api.controller.schema.routerconf_schema import RouterConfSchema
from api.configure.middleware.connectredis import set_to_redis
from api.routercmd.clientcmd.clientcmd import RouterCommandLne
from api.configure.middleware.connectclient import routerapi
from api.modulefn.constants.jwtoken import encode_router
from api.modulefn.constants.respndfn import def_response
from api.modulefn.hashedtxt.AEScipher import AESCipher
from sqlalchemy import or_
from os import getenv
import json

class RouterConfig(object):

	def __init__(self, _id, routerapi):
		self._id 		= _id
		self.routerapi 	= routerapi
		self.errors 	= [False, None, [], {}]

	def find_routerconf_sn(self, serialnumber, routerconf):
		try:
			routerconf = session.query(RouterConf)\
			.filter(or_(RouterConf.serialnumb==serialnumber, RouterConf.id==routerconf)).first()
			schema = RouterConfSchema()
			schema = schema.dump(routerconf)
			return schema
		except Exception as e:
			return False

	def find_routeraccount(self, routerconf):
		try:
			routeraccount = session.query(RouterAccount).filter_by(routerconfid=routerconf).all()
			schemas = RouterAccountSchema(many=True)
			schemas = schemas.dump(routeraccount)
			return schemas
		except Exception as e:
			return False

	def find_routeraccount_id(self, routeraccid):
		try:
			routeraccount = session.query(RouterAccount).filter_by(id=routeraccid).first()
			schema = RouterAccountSchema()
			schema = schema.dump(routeraccount)
			return schema
		except Exception as e:
			return False

	def generate_passwd(self, plaintext):
		try:
			setup = AESCipher(getenv('AESCIPHER'))
			paswd = setup.encrypt(plaintext)
			return paswd
		except Exception as e:
			return False

	def extract_passwd(self, hashed):
		try:
			setup = AESCipher(getenv('AESCIPHER'))
			plain = setup.decrypt(hashed)
			return plain
		except Exception as e:
			return False

	def find_loginuser(self, passwd, username, routeraccount):
		try:
			account = list(filter(lambda x: x['usernamert'] == username, routeraccount))
			if account not in self.errors:
				if self.extract_passwd(account[0]['privatekey']) == passwd:
					data = {
						'username': username,
						'password': account[0]['privatekey']
					}
					return data
				else:
					return False
			else:
				return False
		except Exception as e:
			return False

	def build_router_conf(self,serialnumber,routeros,routeruserid,maxispbandwd):
		response = def_response(topath='build_router_conf')

		try:
			routerconf = self.find_routerconf_sn(serialnumber,None)
			if len(routerconf) != 0:
				response['messag'] = 'serial number have registered'
			else:
				routerconf = RouterConf(serialnumb=serialnumber,routerosve=routeros,
					routeruserid=routeruserid,ispbandwidth=maxispbandwd)
				session.add(routerconf)
				session.commit()
				response['status'] = True
				response['messag'] = 'ok'
		except Exception as e:
			response['messag'] = 'try again'

		return response

	def update_router_conf(self, routerconfid,serialnumber,routeros,routeruserid,maxispbandwd):

		response = def_response(topath='update_router_conf')

		try:
			routerconf = self.find_routerconf_sn(serialnumber, routerconfid)
			if len(routerconf) != 0 and routerconf['id'] == routerconfid:
				session.query(RouterConf).filter(RouterConf.id==routerconf['id'])\
				.update({
					RouterConf.serialnumb: serialnumber if routerconf['serialnumb'] != serialnumber else routerconf['serialnumb'],
					RouterConf.routerosve: routeros if routerconf['routerosve'] != routeros else routerconf['routerosve'],
					RouterConf.routeruserid: routeruserid if routerconf['routeruser']['id'] != routeruserid else routerconf['routeruser']['id'],
					RouterConf.ispbandwidth: maxispbandwd if routerconf['ispbandwidth'] != maxispbandwd else routerconf['ispbandwidth']
					})
				session.commit()
				response['status'] = True
				response['messag'] = 'ok'
			else:
				response['messag'] = 'something wrong'
		except Exception as e:
			response['messag'] = 'try again'

		return response

	def store_router_account(self, username, password, privilage, routerconfid):
		response = def_response(topath='store_router_user')

		try:
			routeraccount = self.find_routeraccount(routerconfid)
			routeraccount = list(filter(lambda x: x['usernamert'] == username, routeraccount))
			if len(routeraccount) != 0:
				response['messag'] = 'please use unique username'
			else:
				paswd = self.generate_passwd(password)
				routr = RouterAccount(usernamert=username,privatekey=paswd,
					privilages=privilage,routerconfid=routerconfid)
				session.add(routr)
				session.commit()
				response['status'] = True
				response['messag'] = 'ok'
		except Exception as e:
			response['messag'] = 'something wrong'

		return response

	def update_ruoter_account(self, routeraccid, username, password, privilage):
		response = def_response(topath='update_router_user')
		try:
			routeraccount = self.find_routeraccount_id(routeraccid)
			if len(routeraccount) != 0:
				paswd = self.generate_passwd(password)
				plain = self.extract_passwd(routeraccount['privatekey'])
				routr = session.query(RouterAccount).filter(RouterAccount.id==routeraccid)\
				.update({
					RouterAccount.usernamert: username if routeraccount['usernamert'] != username else routeraccount['usernamert'],
					RouterAccount.privatekey: paswd if plain != password else routeraccount['privatekey'],
					RouterAccount.privilages: privilage if routeraccount['privilages'] != privilage else routeraccount['privilages']
					})
				session.commit()
				response['status'] = True
				response['messag'] = 'ok'
			else:
				response['messag'] = 'username or password wrong!'
		except Exception as e:
			response['messag'] = 'something wrong'

		return response

	def connect_router_client(self, username, password, ipaddres, userport, rtrcnfid):
		response = def_response(topath='connect_router_client')
		response['tokenq'] = ''
		try:
			rtrconf = self.find_routerconf_sn(None, rtrcnfid)
			if rtrconf not in self.errors:
				account = self.find_loginuser(password, username, rtrconf['routeraccount'])
				print(account)
				if account not in self.errors:
					# connect to router client
					rsapi = routerapi(ipaddres, userport,username,
					account['password'], float(rtrconf['routerosve']))
					# get serial number from router
					setup = RouterCommandLne(rsapi)
					respn = setup.get_serialnumber()
					# store user account in redis

					if respn not in self.errors and\
					respn['serialnumber'] == rtrconf['serialnumb']:
						account['ipaddress'] = ipaddres
						account['userports'] = userport
						account['osversion'] = respn['osversion']
						account['rtrconfid'] = rtrconf['id']
						set_to_redis(f"{rtrconf['id']}_{username}",json.dumps(account))
						# data for token
						tokenq = encode_router(account)
						response['messag'] = 'ok'
						response['status'] = True
						response['tokenq'] = tokenq
					else:
						response['messag'] = 'check serialnumber or account'
				else:
					response['messag'] = 'expired account'
			else:
				response['messag'] = 'expired account'
		except Exception as e:
			response['messag'] = 'something wrong'

		return response