import graphene

class CommonRespd(graphene.ObjectType):
	status 		= graphene.Boolean()
	messag 		= graphene.String()
	topath 		= graphene.String()

class TokenRespd(graphene.ObjectType):
	tokenq		= graphene.String()
	common 		= graphene.Field(CommonRespd)