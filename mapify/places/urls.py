from django.urls import path
from graphene_django.views import GraphQLView
from .views import PlaceSearchView, SavedPlacesView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('search/', PlaceSearchView.as_view(), name='place-search'),
    path('saved/', SavedPlacesView.as_view(), name='saved-places'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql'),
]
