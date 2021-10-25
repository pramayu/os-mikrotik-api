from flask_marshmallow import Marshmallow

ma = Marshmallow()

class RouterAccountSchema(ma.Schema):
	class Meta:
		fields = ("id","usernamert","privatekey","privilages")

class LimitRouterAccountSchema(ma.Schema):
	class Meta:
		fields = ("id","usernamert")