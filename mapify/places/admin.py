from django.contrib import admin
from .models import Place, UserPlaceRelationship

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Admin configuration for the Place model."""
    list_display = ('id', 'name', 'address', 'latitude', 'longitude', 'created_at', 'updated_at')
    search_fields = ('name', 'address')

@admin.register(UserPlaceRelationship)
class UserPlaceRelationshipAdmin(admin.ModelAdmin):
    """Admin configuration for the UserPlaceRelationship model."""
    list_display = ('id', 'user', 'place', 'created_at', 'updated_at')
    search_fields = ('user__username', 'place__name')
    list_filter = ('created_at',)
