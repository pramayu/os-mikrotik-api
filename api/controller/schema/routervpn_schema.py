from flask_marshmallow import Marshmallow

ma = Marshmallow()

class RouterVPNSchema(ma.Schema):
	class Meta:
		fields = ("id","createdt","remoteaddr","uservpn","port")