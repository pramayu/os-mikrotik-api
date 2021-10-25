from flask_marshmallow import Marshmallow

ma = Marshmallow()

class RouterInterfaceSchema(ma.Schema):
	class Meta:
		fields = ("id","name","ipaddress","submask","interface")