import midtransclient
from os import getenv

def paymentstatus(order_id, signkey, status):
	try:
		req = midtransclient.CoreApi(
			is_production = False,
			server_key = getenv('MDTR_SERVER'),
			client_key = getenv('MDTR_KEY')
		)
		res = req.transactions.status(order_id)
		if res['order_id'] == order_id and res['signature_key'] == signkey and res['transaction_status'] == status:
			return True
		else:
			return False
	except Exception as e:
		return False
	