import graphene
from graphene_django.types import DjangoObjectType
from .models import Place, UserPlaceRelationship
from django.contrib.auth.models import User
from graphene import ObjectType, String, Field, List
from graphql_jwt.decorators import login_required

# Define the GraphQL types for Place and User

class PlaceType(DjangoObjectType):
    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'latitude', 'longitude', 'photo_references')

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('username',)

class Query(ObjectType):
    # GraphQL query for retrieving saved places by username
    saved_places_by_user = List(PlaceType, username=String(required=True))

    
    @login_required
    def resolve_saved_places_by_user(self, info, username):
        user = info.context.user  # This gets the user from the request context (after authentication)

        print(f"Authenticated User: {user.username}") 

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception("User not found")
        
        # Get all saved places for this user
        saved_places = UserPlaceRelationship.objects.filter(user=user).select_related('place')

        # Return places in a list
        return [relation.place for relation in saved_places]

# Define the schema
schema = graphene.Schema(query=Query)
