from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Table
from uuid import uuid4
from datetime import datetime, timedelta


engine = create_engine("mysql+pymysql://root:root@localhost/mikrotik")
db_session = scoped_session(sessionmaker(bind=engine))
session = db_session()
Base = declarative_base()

# association_table

routerconf_ports = Table('routerconfports', Base.metadata,
	Column('routerconf', ForeignKey('routerconfs.id'), primary_key=True),
	Column('serviceport', ForeignKey('serviceports.id'), primary_key=True)
)

# class Kamisama(Base):

# 	__tablename__ 	= 'kamisama'
# 	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
# 	username 		= Column(String(32), unique=True, index=True)
# 	password 		= Column(String(254), nullable=False)
# 	emailadd 		= Column(String(50), unique=True, index=True)

class User(Base):

	__tablename__ 	= 'users'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	username 		= Column(String(24), unique=True, index=True)
	password 		= Column(String(255), nullable=False)
	phonenum		= Column(String(18), unique=True, index=True)
	otpdigit 		= Column(String(8), unique=True, index=True)
	activate 		= Column(Boolean(), default=False)
	createdt 		= Column(DateTime(), default=datetime.now())
	userprof 		= relationship("UserProf", back_populates="user")
	routeruser 		= relationship("RouterUser", back_populates="user")
	userinvoice 	= relationship("UserInvoice", back_populates="user")
	transactionsub 	= relationship("TransactionSub", back_populates="user")

# class UserLog
# class UserPref

class UserProf(Base):

	__tablename__ 	= 'userprofs'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	email 			= Column(String(50), unique=True, index=True) 
	fullname 		= Column(String(50))
	businessname 	= Column(String(50))
	userid 			= Column(String(32), ForeignKey("users.id"))
	user 			= relationship("User", back_populates="userprof")

class RouterUser(Base):

	__tablename__ 	= 'routerusers'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	routername 		= Column(String(32))
	startdate		= Column(DateTime())
	endeddate 		= Column(DateTime())
	expstatus		= Column(Boolean(), default=False)
	userid 			= Column(String(32), ForeignKey('users.id'), index=True)
	user 			= relationship("User", back_populates="routeruser")
	routervpn 		= relationship("RouterVPN", back_populates="routeruser")
	routerconf 		= relationship("RouterConf", back_populates="routeruser")

class ServicePort(Base):

	__tablename__ 	= 'serviceports'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	name 			= Column(String(32), nullable=False)
	port 			= Column(String(255))
	image 			= Column(String(255))
	routerconf 		= relationship("RouterConf", secondary=routerconf_ports,
						back_populates="serviceport")

class RouterConf(Base):

	__tablename__ 	= 'routerconfs'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	serialnumb 		= Column(String(20), unique=True, index=True)
	routerosve 		= Column(String(20))
	ispbandwidth 	= Column(String(20))
	routeruserid 	= Column(String(32), ForeignKey("routerusers.id"))
	routeruser 		= relationship("RouterUser", back_populates="routerconf")
	serviceprovide 	= relationship("ServicesProvided", back_populates="routerconf") #PPPoE Client
	serviceport 	= relationship("ServicePort", secondary=routerconf_ports,
						back_populates="routerconf")
	bandwidth 		= relationship("Bandwidth", back_populates="routerconf")
	routeraccount 	= relationship("RouterAccount", back_populates="routerconf")
	routerinterface	= relationship("RouterInterface", back_populates="routerconf")

class RouterAccount(Base):

	__tablename__ 	= 'routeraccounts'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	usernamert 		= Column(String(32), nullable=False)
	privatekey 		= Column(String(255))
	privilages 		= Column(String(20))
	routerconfid 	= Column(String(32), ForeignKey('routerconfs.id'))
	routerconf 		= relationship("RouterConf", back_populates="routeraccount")

class DivideBandwidth(Base):

	__tablename__ 	= 'dividebandwidths'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	namefor 		= Column(String(32))
	maxdownload 	= Column(String(32))
	maxupload 		= Column(String(32))
	bandwidthid 	= Column(String(32), ForeignKey("bandwidths.id"))
	bandwidth		= relationship("Bandwidth", back_populates="dividebandwidth")

class Bandwidth(Base):

	__tablename__ 	= 'bandwidths'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	namefor			= Column(String(32))
	maxdownload 	= Column(String(20))
	maxupload 		= Column(String(20))
	serviceprovide 	= relationship("ServicesProvided", back_populates="bandwidth")
	routerconfid	= Column(String(32), ForeignKey("routerconfs.id"))
	routerconf 		= relationship("RouterConf", back_populates="bandwidth")
	dividebandwidth = relationship("DivideBandwidth", back_populates="bandwidth")

class ServicesProvided(Base): #PPPoE Client

	__tablename__ 	= 'serviceprovides'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	servicename 	= Column(String(32), nullable=False)
	pricing 		= Column(String(32))
	duration 		= Column(DateTime())
	bandwidthid 	= Column(String(32), ForeignKey("bandwidths.id"))
	bandwidth 		= relationship("Bandwidth", back_populates="")
	routerconfid 	= Column(String(32), ForeignKey('routerconfs.id'))
	routerconf 		= relationship("RouterConf", back_populates="serviceprovide")
	subscriptionclient 	= relationship("SubscriberClient", back_populates="serviceprovide")
	voucherhotspot 	= relationship("VoucerHotspot", back_populates="serviceprovide")

class SubscriberClient(Base):

	__tablename__ 	= 'subscriberclients'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	fullname 		= Column(String(32))
	phone 			= Column(String(18))
	address 		= Column(Text())
	serviceprovideid 	= Column(String(32), ForeignKey("serviceprovides.id"))
	serviceprovide 	= relationship("ServicesProvided", back_populates="subscriptionclient")
	accesspointprof = relationship("AccessPointProf", back_populates="subscriptionclient")

class AccessPointProf(Base):

	__tablename__ 	= 'accesspoints'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	username 		= Column(String(32), unique=True, index=True)
	password 		= Column(String(255), nullable=False)
	serialnumb 		= Column(String(20), unique=True)
	subscriptionclientid = Column(String(32), ForeignKey("subscriberclients.id"))
	subscriptionclient 	= relationship("SubscriberClient", back_populates="accesspointprof")

class VoucerHotspot(Base):

	__tablename__ 	= 'hotspotvouchers'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	username 		= Column(String(32))
	password 		= Column(String(100))
	servicepaid 	= Column(String(32), ForeignKey("serviceprovides.id"))
	serviceprovide 	= relationship("ServicesProvided", back_populates="voucherhotspot")

class RouterVPNProfile(Base):

	__tablename__ 	= 'routervpnprofiles'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	profilename 	= Column(String(32), unique=True)
	status 			= Column(Boolean(), default=False, index=True)
	routervpns 		= relationship("RouterVPN", back_populates="routervpnprofile")
	l2tpsecret 		= Column(String(255))
	iphost 			= Column(String(20))
	localaddr 		= Column(String(18), index=True)

class RouterVPN(Base):

	__tablename__ 	= 'routervpns'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	uservpn 		= Column(String(32), index=True)
	privatekey 		= Column(String(255))
	createdt 		= Column(DateTime(), default=datetime.utcnow())
	remoteaddr 		= Column(String(18), unique=True, index=True)
	routeruserid	= Column(String(32), ForeignKey("routerusers.id"))
	port 			= Column(String(8))
	routeruser		= relationship("RouterUser", back_populates="routervpn")
	routervpnprofileid = Column(String(32), ForeignKey('routervpnprofiles.id'))
	routervpnprofile = relationship("RouterVPNProfile", back_populates="routervpns")

class PaymentMethod(Base):

	__tablename__ 	= 'paymentmethods'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	kode 			= Column(String(20))
	name 			= Column(String(32))
	paytype 		= Column(String(20)) #transfer_bank, gopay, echannel, permata
	icon 			= Column(String(100))
	tax 			= Column(String(20))
	status 			= Column(Boolean(), default=True)
	userinvoice 	= relationship("UserInvoice", back_populates="paymentmethod")

class PlanPrice(Base):

	__tablename__ 	= 'planprices'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	periode 		= Column(String(32))
	pricing 		= Column(String(32))
	discount 		= Column(String(32), ForeignKey("discounts.id"))
	givendis 		= relationship("Discount", back_populates="planprice")
	userinvoice 	= relationship("UserInvoice", back_populates="planprice")

class Discount(Base):

	__tablename__ 	= 'discounts'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	number 			= Column(String(5), nullable=False)
	speriode 		= Column(DateTime(), default=datetime.now())
	eperiode 		= Column(DateTime())
	status 			= Column(Boolean(), default=False)
	createdt 		= Column(DateTime(), default=datetime.now())
	updatedt 		= Column(DateTime())
	quantity 		= Column(String(3)) #person
	planprice 		= relationship("PlanPrice", back_populates="givendis")

class UserInvoice(Base):

	__tablename__ 	= 'userinvoices'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	paidst 			= Column(Boolean(), default=False, index=True)
	totalamount 	= Column(String(32))
	createdt 		= Column(DateTime(), default=datetime.now())
	updatedt 		= Column(DateTime())
	paymentmethodid = Column(String(32), ForeignKey('paymentmethods.id'))
	paymentmethod 	= relationship("PaymentMethod", back_populates="userinvoice")
	planpriceid 	= Column(String(32), ForeignKey('planprices.id'))
	planprice 		= relationship("PlanPrice", back_populates="userinvoice")
	userid 			= Column(String(32), ForeignKey('users.id'))
	user 			= relationship("User", back_populates="userinvoice")
	transactionsub 	= relationship("TransactionSub", back_populates="userinvoice")
	typeorder 		= Column(String(10), default='firstime')

class TransactionSub(Base):

	__tablename__ 	= 'transactionsubs'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	status 			= Column(String(20)) #success, failure, pending
	transactiontime = Column(DateTime())
	va_number		= Column(String(30), index=True)
	kode 		 	= Column(String(20))
	qr_code 		= Column(String(200))
	merchant_id 	= Column(String(40))
	userinvoiceid 	= Column(String(32), ForeignKey("userinvoices.id"), index=True)
	userid 			= Column(String(32), ForeignKey("users.id"))
	userinvoice 	= relationship("UserInvoice", back_populates="transactionsub")
	user 			= relationship("User", back_populates="transactionsub")

class RouterInterface(Base):

	__tablename__ 	= 'routerinterfaces'
	id 				= Column(String(32), primary_key=True, default=uuid4().hex)
	name 			= Column(String(20), unique=True, index=True)
	interface 		= Column(String(20))
	ipaddress  		= Column(String(20), unique=True, index=True)
	submask 		= Column(String(30))
	routerconfid 	= Column(String(32), ForeignKey('routerconfs.id'))
	routerconf 		= relationship("RouterConf", back_populates="routerinterface")




Base.metadata.create_all(engine)