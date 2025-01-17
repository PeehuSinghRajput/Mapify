from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Place, UserPlaceRelationship
from .utils import search_places

class PlaceSearchView(APIView):
    """
    API view to search for places using the Google Places API and save them.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"error": "Query parameter is required"}, status=400)

        # Search places using the Google Places API
        data = search_places(query)
        if "error" in data:
            return Response({"error": data["error"]}, status=500)

        # Simplify response and save places to the database and Neo4j
        results = []
        for place in data.get("results", []):
            place_name = place.get("name")
            place_address = place.get("formatted_address")
            latitude = place.get("geometry", {}).get("location", {}).get("lat")
            longitude = place.get("geometry", {}).get("location", {}).get("lng")
            photo_references = [photo.get("photo_reference") for photo in place.get("photos", [])]

            # Check if place already exists
            existing_place, created = Place.objects.get_or_create(
                name=place_name,
                defaults={
                    'address': place_address,
                    'latitude': latitude,
                    'longitude': longitude,
                    'photo_references': photo_references
                }
            )

            if created:
                # Save to Neo4j if new place
                existing_place.save_to_neo4j()

            # Create UserPlaceRelationship
            user_place, created = UserPlaceRelationship.objects.get_or_create(
                user=request.user,
                place=existing_place
            )

            results.append({
                "name": existing_place.name,
                "address": existing_place.address,
                "location": {"lat": existing_place.latitude, "lng": existing_place.longitude},
                "photo_reference": existing_place.photo_references[0] if existing_place.photo_references else None,
            })

        return Response({"places": results}, status=200)


class SavedPlacesView(APIView):
    """
    API view to retrieve saved places for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all saved places for the logged-in user
        saved_places = UserPlaceRelationship.objects.filter(user=request.user).select_related('place')

        # Prepare response data
        results = []
        for relation in saved_places:
            place = relation.place
            results.append({
                "id": place.id,
                "name": place.name,
                "address": place.address,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "photo_references": place.photo_references,
                "saved_at": relation.created_at,
            })

        return Response({"saved_places": results}, status=200)
