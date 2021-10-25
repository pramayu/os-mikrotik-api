import graphene
from api.controller.service import MainService
from api.controller.queries.userdata.catchuser import CatchUserData


class Query(CatchUserData, graphene.ObjectType):
	pass

class Mutation(MainService, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query, mutation=Mutation)