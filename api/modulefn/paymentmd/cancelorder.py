import midtransclient
from os import getenv

def cancelsubscribe(invoiceid):
	try:
		req = midtransclient.CoreApi(
			is_production = False,
			server_key = getenv('MDTR_SERVER'),
			client_key = getenv('MDTR_KEY')
		)
		req.transactions.cancel(invoiceid)
	except Exception as e:
		return False