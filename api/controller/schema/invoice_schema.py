from flask_marshmallow import Marshmallow
from api.controller.schema.planprice_schema import PlanPriceSchema
from api.controller.schema.paidmethod_schema import PaymentMethodSchema
from api.controller.schema.user_schema import UserLimitSchema
from api.controller.schema.transaction_schema import TransactionSubSchema

ma = Marshmallow()

class InvoiceSchema(ma.Schema):
	transactionsub = ma.Nested(TransactionSubSchema)
	paymentmethod = ma.Nested(PaymentMethodSchema)
	# planprice = ma.Nested(PlanPriceSchema)
	user = ma.Nested(UserLimitSchema)
	class Meta:
		fields = ("id","totalamount","paymentmethod","user","transactionsub","typeorder","updatedt")

class InvoicePlanPriceSchema(ma.Schema):
	planprice = ma.Nested(PlanPriceSchema)
	user = ma.Nested(UserLimitSchema)
	class Meta:
		fields = ("id","totalamount","user","typeorder","planprice")