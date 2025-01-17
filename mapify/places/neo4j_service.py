from neo4j import GraphDatabase
import logging
from django.conf import settings

# Logger setup
logger = logging.getLogger(__name__)

class Neo4jService:
    """Service for interacting with the Neo4j database."""

    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def create_place(self, name, address, latitude, longitude, photo_references):
        """Create a new place node in Neo4j."""
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_place_transaction,
                name,
                address,
                latitude,
                longitude,
                photo_references,
            )
        return result

    @staticmethod
    def _create_place_transaction(tx, name, address, latitude, longitude, photo_references):
        query = """
        CREATE (p:Place {
            name: $name,
            address: $address,
            latitude: $latitude,
            longitude: $longitude,
            photo_references: $photo_references
        })
        RETURN p
        """
        result = tx.run(query, name=name, address=address, latitude=latitude, longitude=longitude, photo_references=photo_references)
        return result.single()

    def find_places_by_user(self, username):
        """Retrieve places saved by a specific user."""
        with self.driver.session() as session:
            result = session.read_transaction(self._find_places_transaction, username)
        return result

    @staticmethod
    def _find_places_transaction(tx, username):
        query = """
        MATCH (u:User {username: $username})-[:SAVED]->(p:Place)
        RETURN p
        """
        result = tx.run(query, username=username)
        return [record["p"] for record in result]
