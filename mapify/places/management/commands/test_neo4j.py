from django.core.management.base import BaseCommand
from places.neo4j_service import Neo4jService

class Command(BaseCommand):
    help = "Test Neo4j connection and functionality."

    def handle(self, *args, **kwargs):
        service = Neo4jService()

        # Test creating a place
        print("Creating a test place in Neo4j...")
        service.create_place(
            name="Test Place",
            address="123 Test Street",
            latitude=40.7128,
            longitude=-74.0060,
            photo_references=["photo1", "photo2"],
        )

        print("Fetching places for a test user...")
        places = service.find_places_by_user("testuser")
        print(places)

        service.close()
