from flask_marshmallow import Marshmallow
from api.filemodel.db import PaymentMethod
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

ma = Marshmallow()

class PaymentMethodSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = PaymentMethod
		include_relationships = True
