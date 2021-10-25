import hashlib
import midtransclient
from os import getenv

def verify_signature(json_data):
	req = midtransclient.CoreApi(
		is_production = False,
		server_key = getenv('MDTR_SERVER'),
		client_key = getenv('MDTR_KEY')
	)

	payload = {}

	try:
		response = req.transactions.notification(json_data)
		plaintxt = response['order_id'] + response['status_code'] + response['gross_amount'] + getenv('MDTR_SERVER')
		hashed = hashlib.sha512(plaintxt.encode('utf-8'))
		if response['signature_key'] == hashed.hexdigest():
			payload['status'] =''
			payload['va_numbers'] = ''
			payload['qrkode'] = ''
			payload['merchant_id'] = response['merchant_id']
			payload['invoiceid'] = response['order_id']
			payload['signature_key'] = response['signature_key']
			payload['transaction_status'] = response['transaction_status']
			payload['status_code'] = response['status_code']
			payload['transactiontime'] = response['transaction_time']
			if response['transaction_status'] == 'settlement' or response['transaction_status'] == 'capture':
				payload['status'] = 'success'
			elif response['transaction_status'] == 'cancel' or response['transaction_status'] == 'deny' or response['transaction_status'] == 'expire':
				payload['status'] = 'failure'
			elif response['transaction_status'] == 'pending':
				payload['status'] = 'pending'

			if response['payment_type'] == 'bank_transfer':
				if 'va_numbers' in response:
					payload['kode'] = response['va_numbers'][0]['bank']
					payload['va_number'] = response['va_numbers'][0]['va_number']
				if 'permata_va_number' in response:
					payload['kode'] = ''
					payload['va_number'] = response['permata_va_number']
			if response['payment_type'] == 'echannel':
				payload['va_number'] = response['bill_key']
				payload['kode'] = response['biller_code']
			elif response['payment_type'] == 'gopay':
				payload['kode'] = response['payment_type']
				payload['qrkode'] = response['transaction_id']
			elif response['payment_type'] == 'cstore':
				payload['va_number'] = response['payment_code']
				payload['kode'] = response['store']
			return payload
		else:
			return False
	except Exception as e:
		print(e)
		return False