from flask_marshmallow import Marshmallow
from api.controller.schema.routeruser_schema import RouterUserSchema
from api.controller.schema.routeraccount_schema import RouterAccountSchema

ma = Marshmallow()

class RouterConfSchema(ma.Schema):
	routeruser = ma.Nested(RouterUserSchema)
	routeraccount = ma.Nested(RouterAccountSchema(many=True))
	class Meta:
		fields = ("id","serialnumb","routerosve","ispbandwidth","routeruser","routeraccount")

class RouterConfxRouterUserSchema(ma.Schema):
	routeruser = ma.Nested(RouterUserSchema)
	class Meta:
		fields = ("id", "routeruser")
