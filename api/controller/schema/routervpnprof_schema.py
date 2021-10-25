from flask_marshmallow import Marshmallow

ma = Marshmallow()

class RouterVPNProfSchema(ma.Schema):
	class Meta:
		fields = ("id","profilename","status","localaddr","iphost","port")