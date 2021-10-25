from api.filemodel.db import session, User, RouterUser, RouterVPN, UserInvoice, RouterVPNProfile
from api.controller.schema.routervpnprof_schema import RouterVPNProfSchema
from api.controller.schema.routeruser_schema import RouterUserSchema
from api.controller.schema.routervpn_schema import RouterVPNSchema
from api.controller.schema.invoice_schema import InvoicePlanPriceSchema
from api.modulefn.constants.respndfn import def_response
from api.modulefn.hashedtxt.AEScipher import AESCipher
from datetime import datetime, timedelta
from sqlalchemy import desc
from uuid import uuid4
from os import getenv

class ConfigureVPN(object):

	def __init__(self, api):
		self.api 	= api

	def find_userinvoice(self, _id):
		try:
			userinvoice = session.query(UserInvoice).filter_by(id=_id).first()
			schema = InvoicePlanPriceSchema()
			schema = schema.dump(userinvoice)
			return schema
		except Exception as e:
			return False

	def find_routervpnprof(self):
		try:
			vpnprofile = session.query(RouterVPNProfile).filter_by(status=True).first()
			schema = RouterVPNProfSchema()
			schema = schema.dump(vpnprofile)
			return schema
		except Exception as e:
			return False

	def find_lastroutervpn(self):
		try:
			routervpn = session.query(RouterVPN).order_by(desc(RouterVPN.createdt)).first()
			schema = RouterVPNSchema()
			schema = schema.dump(routervpn)
			return schema
		except Exception as e:
			return False

	def encrypt_passwd(self, plaintext):
		try:
			cipher = getenv('AESCIPHER')
			setup = AESCipher(cipher)
			encrypt = setup.encrypt(plaintext)
			return encrypt
		except Exception as e:
			return False

	def remoteport(self, port):
		exclude = ['8728','8729','8291']
		try:
			nextport = int(port) + 1
			if str(nextport) in exclude:
				return remoteport(str(nextport))
			return str(nextport)
		except Exception as e:
			return False

	def remoteaddr(self,ipaddress):
	    try:
	        addr_list = ipaddress.split('.')
	        netw_addr = '.'.join(addr_list[:3])
	        host_addr = f"{netw_addr}.{int(addr_list[3]) + 1}"
	        if int(host_addr.split('.')[-1]) == 255:
	            edit_netw = int(addr_list[2]) + 1
	            host_addr = '.'.join(addr_list[:2])
	            host_addr = f"{host_addr}.{str(edit_netw)}.1"
	        return host_addr
	    except Exception as e:
	        return False



	def fetch_routerl2tp(self, username, passwd, profile, remoteaddr, localaddr):
		try:
			fetch = self.api.get_resource('ppp/secret/')
			fetch.add(name=username,password=passwd,profile=profile,
				local_address=localaddr,remote_address=remoteaddr,
				service='l2tp',disabled='no')
			return True
		except Exception as e:
			return False

	def fetch_chrfirewall(self, iphost, port, remoteaddr, username):
	 	try:
	 		fetch = self.api.get_resource('ip/firewall/nat/')
	 		fetch.add(chain='dstnat',dst_address=iphost,dst_port=port,
	 			action='dst-nat',to_addresses=remoteaddr,to_ports='8728',
	 			protocol='tcp',comment=f"{username}/{remoteaddr}")
	 	except Exception as e:
	 		return False


	def build_routeruser(self, userid, planperiode):
		response = def_response(topath='build_routeruser')
		try:
			startdate = datetime.utcnow()
			endeddate = datetime.utcnow() + timedelta(days=(int(planperiode) * 31) + 5)
			routernme = f"router-{uuid4().hex[:4]}"
			routerusr = RouterUser(startdate=startdate, endeddate=endeddate, userid=userid, routername=routernme)
			session.add(routerusr)
			session.commit()
			schema = RouterUserSchema()
			router = schema.dump(routerusr) 
			return router
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'
		return response


	def build_uservpnv(self,routeruser,tempasswd,vpnprof,remoteaddr,encryptpw,port):
		username = uuid4().hex[:8]
		try:
			vpn = RouterVPN(uservpn=username,privatekey=encryptpw,remoteaddr=remoteaddr,
			routeruserid=routeruser,routervpnprofileid=vpnprof['id'],port=port)
			session.add(vpn)
			session.commit()
			status = self.fetch_routerl2tp(username,tempasswd,vpnprof['profilename'], remoteaddr,vpnprof['localaddr'])
			if status == True:
				self.fetch_chrfirewall(vpnprof['iphost'],port,remoteaddr, username)
			else:
				return False
		except Exception as e:
			print(e)
			return False


	def build_uservpn(self, routeruser):
		response = def_response(topath='build_uservpn')
		try:
			routervpn = self.find_lastroutervpn()
			if routervpn != None:
				vpnprof = self.find_routervpnprof()
				tempasswd = uuid4().hex[:8]
				encryptpw = self.encrypt_passwd(tempasswd)
				if len(routervpn) == 0 and len(vpnprof) != 0:
					remoteaddr = '.'.join(vpnprof['localaddr'].split('.')[:3]) + ".2"
					self.build_uservpnv(routeruser,tempasswd,vpnprof,remoteaddr,encryptpw,'1000')
				elif len(routervpn) != 0 and len(vpnprof) != 0:
					remoteaddr = self.remoteaddr(routervpn['remoteaddr'])
					remoteport = self.remoteport(routervpn['port'])
					self.build_uservpnv(routeruser,tempasswd,vpnprof,remoteaddr,encryptpw, remoteport)
				else:
					response['messag'] = 'something wrong'
			else:
				response['messag'] = 'something wrong'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'
		return response


	def buildvpnschedule(self, _id):
		response = def_response(topath='buildvpnschedule')
		try:
			invoice = self.find_userinvoice(_id)
			if invoice != None:
				if invoice['typeorder'] == 'firstime':
					payload = self.build_routeruser(invoice['user']['id'], invoice['planprice']['periode'])
					if payload != None:
						self.build_uservpn(payload['id'])
						response['status'] = True
						response['messag'] = 'ok'
					else:
						response['messag'] = 'something wrong'
				if invoice['typeorder'] == 'upgraded':
					pass
			else:
				response['messag'] = 'order not found'
		except Exception as e:
			response['messag'] = 'something wrong'
		return response