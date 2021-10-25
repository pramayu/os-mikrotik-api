from api.filemodel.db import session, User, PaymentMethod, PlanPrice, UserInvoice,TransactionSub
from api.controller.schema.paidmethod_schema import PaymentMethodSchema
from api.controller.schema.transaction_schema import TransactionSubSchema
from api.controller.schema.planprice_schema import PlanPriceSchema
from api.controller.schema.invoice_schema import InvoiceSchema
from api.modulefn.paymentmd.cancelorder import cancelsubscribe
from api.modulefn.constants.respndfn import def_response
from api.modulefn.paymentmd.midtrans import midtranspayment
from sqlalchemy import or_, and_
from datetime import datetime
from uuid import uuid4

class PaymentConfig(object):

	def __init__(self, _id):
		self._id 	= _id

	def find_planprice(self, _id):
		try:
			planprice = session.query(PlanPrice).filter_by(id=_id).first()
			schema = PlanPriceSchema()
			schema = schema.dump(planprice)
			return schema
		except Exception as e:
			return False

	def find_paymenentmethod(self, _id):
		try:
			paidmethod = session.query(PaymentMethod).filter_by(id=_id).first()
			schema = PaymentMethodSchema()
			schema = schema.dump(paidmethod)
			return schema
		except Exception as e:
			return False

	def find_userinvoice(self, _id):
		try:
			userinvoice = session.query(UserInvoice).filter_by(id=_id).first()
			schema = InvoiceSchema()
			schema = schema.dump(userinvoice)
			return schema
		except Exception as e:
			return False

	def find_transaction(self, invoice_id, status):
		try:
			transaction = session.query(TransactionSub)\
			.filter(and_(TransactionSub.userinvoiceid==invoice_id, TransactionSub.status==status)).first()
			schema = TransactionSubSchema()
			schema = schema.dump(transaction)
			return schema
		except Exception as e:
			return False

	def totalamount(self, id):
		try:
			planprice = self.find_planprice(id)
			totalamount = 0
			discount = planprice['givendis']
			if discount['status'] == True and discount['number'] != 0:
				totalamount = ((100 - float(discount['number'])) / 100)
				totalamount = totalamount * float(planprice['pricing'])
			else:
				totalamount = float(planprice['pricing'])
			payloads = {
				'totalamount': str(totalamount),
				'urplanprice': planprice['id']
			}
			return payloads
		except Exception as e:
			return False

	def besubscriber(self, planprice, payments):

		response = def_response(topath='besubscriber')
		try:
			paidplan = self.totalamount(planprice)
			payments = self.find_paymenentmethod(payments)
			invoceid = UserInvoice(
				totalamount=paidplan['totalamount'],\
				paymentmethodid=payments['id'], planpriceid=paidplan['urplanprice'],\
				userid=self._id
			)
			session.add(invoceid)
			session.commit()
			response['status'] = True
			response['messag'] = 'ok'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'

		return response

	def payoutorder(self, invoice):

		response = def_response(topath='payoutorder')
		try:
			invoice = self.find_userinvoice(invoice)
			if invoice != None:
				payload = {
					'invoice': invoice['id'],
					'payment_type': invoice['paymentmethod']['paytype'],
					'amount': float(invoice['totalamount']) + float(invoice['paymentmethod']['tax']),
					'kode': invoice['paymentmethod']['kode'],
					'username': invoice['user']['username'],
					'phone': invoice['user']['phonenum']
				}
				result = midtranspayment(payload)
				response['status'] = True
				response['messag'] = 'ok'
			else:
				response['messag'] = 'please order first'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'

		return response

	def create_transaction(self, invoice, payload):
		response = def_response(topath='create_transaction')
		try:
			if invoice != None and invoice['updatedt'] == None:
				if invoice['transactionsub'] == None or len(invoice['transactionsub']) == 0:
					trans = TransactionSub(status=payload['status'],\
					transactiontime=payload['transactiontime'],\
					va_number=payload['va_number'],kode=payload['kode'],\
					qr_code=payload['qrkode'],userinvoiceid=payload['invoiceid'],\
					userid=invoice['user']['id'],merchant_id=payload['merchant_id'])
					session.add(trans)
					session.commit()

					response['status'] = True
					response['messag'] = 'ok'
				else:
					response['messag'] = 'transaction already exist'
			else:
				response['messag'] = 'order not found'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'

		return response

	def update_transaction(self, payload, trans):
		response = def_response(topath='update_transaction')
		try:
			if trans != None:
				if trans['userinvoice'] != None or len(trans['userinvoice']) != 0:
					session.query(TransactionSub)\
					.filter(TransactionSub.id==trans['id'])\
					.update({TransactionSub.status: payload['transaction_status']})
					session.query(UserInvoice)\
					.filter(UserInvoice.id==trans['userinvoice'])\
					.update({
						UserInvoice.paidst: True if payload['transaction_status'] == 'settlement' else False,
						UserInvoice.updatedt: datetime.utcnow()})
					session.commit()

					response['status'] = True
					response['messag'] = 'ok'
				else:
					response['messag'] = 'order not found'
			else:
				response['messag'] = 'transaction not found'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'
		return response
		

	def transactionsubs(self, payload):
		response = def_response(topath='transactionsubs')
		try:
			if payload['status'] == 'pending':
				invoicez = self.find_userinvoice(payload['invoiceid'])
				response = self.create_transaction(invoicez, payload)
			elif payload['status'] in ['failure','success','capture']:
				trans = self.find_transaction(payload['invoiceid'], 'pending')
				response = self.update_transaction(payload, trans)
			else:
				response['messag'] = 'try again'
		except Exception as e:
			print(e)
			response['messag'] = 'something wrong'
		return response

	def cancelorder(self, orderid):
		response = def_response(topath='cancelorder')
		try:
			trans = self.find_transaction(orderid, 'pending')
			if trans['user']['id'] == self._id:
				cancelsubscribe(trans['userinvoice'])
				response['status'] = True
				response['messag'] = 'ok'
			else:
				response['messag'] = 'order not found'
		except Exception as e:
			response['messag'] = 'something wrong'

		return response