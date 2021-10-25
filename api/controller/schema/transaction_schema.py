from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.filemodel.db import TransactionSub
from api.controller.schema.user_schema import UserLimitSchema

ma = Marshmallow()

class TransactionSubSchema(SQLAlchemyAutoSchema):
	user = ma.Nested(UserLimitSchema)
	class Meta:
		model = TransactionSub
		include_relationships = True