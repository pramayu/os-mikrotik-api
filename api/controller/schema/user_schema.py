from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserSchema(ma.Schema):
	class Meta:
		fields = ("id","username","password","activate","phonenum")

class UserLimitSchema(ma.Schema):
	class Meta:
		fields = ("id","username","phonenum")