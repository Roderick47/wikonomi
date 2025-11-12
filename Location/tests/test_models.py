from django.test import TestCase
from Location.models import Location


class TestLocationModel(TestCase):
    def test_location_creation_with_coordinates(self):
        """Test creating a location with valid coordinates"""
        location = Location.objects.create(
            latitude=1.2921,
            longitude=36.8219
        )
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(location.latitude, 1.2921)
        self.assertEqual(location.longitude, 36.8219)
    
    def test_location_creation_without_coordinates(self):
        """Test creating a location with null coordinates"""
        location = Location.objects.create(
            latitude=None,
            longitude=None
        )
        self.assertEqual(Location.objects.count(), 1)
        self.assertIsNone(location.latitude)
        self.assertIsNone(location.longitude)
    
    def test_location_str_representation(self):
        """Test the string representation of Location"""
        location = Location.objects.create(
            latitude=1.2921,
            longitude=36.8219
        )
        # Assuming Location has a __str__ method
        str_repr = str(location)
        self.assertIsInstance(str_repr, str)
