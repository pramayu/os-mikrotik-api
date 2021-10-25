import graphene

class CatchUserData(graphene.ObjectType):

	user = graphene.String()

	def resolve_user(root, info, **kwargs):
		pass