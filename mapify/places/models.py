from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from py2neo import Graph, Node

class TimestampedModel(models.Model):
    """Abstract base model to add created and updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Place(TimestampedModel):
    """Model to store information about a place."""
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo_references = models.JSONField()  # To store image references (list of strings)

    def __str__(self):
        return self.name

    def save_to_neo4j(self):
        """Save the place to Neo4j database."""
        graph = Graph(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
        
        # Create a Place node in Neo4j
        place_node = Node("Place", name=self.name, address=self.address,
                          latitude=self.latitude, longitude=self.longitude,
                          photo_references=self.photo_references)
        
        graph.create(place_node)
        return place_node

class UserPlaceRelationship(TimestampedModel):
    """Model to store the relationship between a user and a place."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='users')

    class Meta:
        unique_together = ('user', 'place')  # Ensure a user can't save the same place multiple times

    def __str__(self):
        return f"{self.user.username} -> {self.place.name}"
