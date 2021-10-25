from flask_marshmallow import Marshmallow
from api.controller.schema.user_schema import UserLimitSchema

ma = Marshmallow()

class RouterUserSchema(ma.Schema):
	user = ma.Nested(UserLimitSchema)
	class Meta:
		fields = ("id","user")