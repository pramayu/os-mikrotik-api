from flask_marshmallow import Marshmallow
from api.filemodel.db import PlanPrice
from api.controller.schema.discount_schema import DiscountSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

ma = Marshmallow()

class PlanPriceSchema(SQLAlchemyAutoSchema):
	givendis = ma.Nested(DiscountSchema)
	class Meta:
		model = PlanPrice
		include_relationships = True
	