from api.modulefn.hashedtxt.sha512 import verify_signature
from api.modulefn.paymentmd.confirm import paymentstatus
from api.modulefn.constants.setupvpn import configurevpn
from api.filemodel.db_payment import PaymentConfig
from api.modulefn.constants.jwtoken import chr_api
from flask import Blueprint, abort, request
import hashlib

webhook_receive = Blueprint('endpoint',__name__)

@webhook_receive.route('/endpoint', methods=['POST'])
def endpoint():
	if request.method == 'POST':
		try:
			res = verify_signature(request.json)
			if paymentstatus(res['invoiceid'],res['signature_key'],res['transaction_status']):
				setup = PaymentConfig(None)
				respd = setup.transactionsubs(res)
				if (res['transaction_status'] == 'settlement' or res['transaction_status'] == 'capture'  and respd['status'] == True):
					token = chr_api('settlement')
					configurevpn(res, token)
				return 'Success', 200
			else:
				return 'Unauthorized', 401
		except Exception as e:
			return 'Bad Request', 400
	else:
		abort(400)
