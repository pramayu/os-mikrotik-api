from flask_marshmallow import Marshmallow
from api.filemodel.db import Discount
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

ma = Marshmallow()

class DiscountSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Discount