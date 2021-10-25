import midtransclient
from os import getenv
from api.modulefn.constants.respndfn import def_response

def midtranspayment(data):

	response = def_response(topath='paid upgrade')
	response['charge'] = ''
	exclude = ['permata']

	req = midtransclient.CoreApi(
		is_production = False,
		server_key = getenv('MDTR_SERVER'),
		client_key = getenv('MDTR_KEY')
	)

	def switching(argument, data):
		# argument["payment_type"] = data['payment_type']
		switcher = {
			'bank_transfer'	: {"bank": data['kode']},
			'gopay'		: {"enable_callback": False},
			'cstore'		: {"store": data['kode'], "message" : "Thank you."},
			'echannel'		: {"bill_info1" : data['username'],
						 "bill_info2": str(data['amount'])}
		}
		return switcher.get(argument)

	if len(data) != 0:
		argument = {
			"payment_type": data['payment_type'],
			"transaction_details": {
				"gross_amount": str(data['amount']),
				"order_id": data['invoice']
			},
			"customer_details": {
				"first_name": data['username'],
				"phone": data['phone']
			},
		}
		if data['payment_type'] not in exclude:
			argument[f"{data['payment_type']}"] = switching(data['payment_type'], data)
		print(argument)
		try:
			charge = req.charge(argument)
			if charge:
				response['messag'] = 'ok'
				response['status'] = True
				response['charge'] = charge
			else:
				response['messag'] = 'try again'
		except Exception as e:
			print(e)
			response['messag'] = 'try again'
	else:
		response['messag'] = 'try again'

	return response


	"""
"custom_expiry": {
      "order_time": "2016-12-07 11:54:12 +0700",
      "expiry_duration": 60,
      "unit": "minute"
  }
	"""