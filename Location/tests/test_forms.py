from django.test import TestCase
from Location.forms import LocationForm
from Location.models import Location


class TestLocationForm(TestCase):
    def test_form_with_coordinates_and_browser_location(self):
        """Test form validation with coordinates and use_browser_location=True"""
        form = LocationForm(data={
            'latitude': 1.2921,
            'longitude': 36.8219,
            'use_browser_location': True
        })
        self.assertTrue(form.is_valid())
    
    def test_form_with_coordinates_without_browser_location(self):
        """Test form validation with coordinates and use_browser_location=False"""
        form = LocationForm(data={
            'latitude': 1.2921,
            'longitude': 36.8219,
            'use_browser_location': False
        })
        self.assertTrue(form.is_valid())
    
    def test_form_with_address_only(self):
        """Test form validation with address only"""
        form = LocationForm(data={
            'address': '123 Main Street, Nairobi',
            'use_browser_location': False
        })
        self.assertTrue(form.is_valid())
    
    def test_form_with_browser_location_but_no_coordinates(self):
        """Test form validation fails when use_browser_location=True but no coordinates"""
        form = LocationForm(data={
            'use_browser_location': True
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Please allow browser location access', str(form.errors))
    
    def test_form_without_browser_location_and_no_data(self):
        """Test form validation fails when no coordinates or address provided"""
        form = LocationForm(data={
            'use_browser_location': False
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Please provide either coordinates or an address', str(form.errors))
    
    def test_form_with_zero_coordinates(self):
        """Test that zero coordinates (0.0, 0.0) are treated as falsy and fail validation"""
        form = LocationForm(data={
            'latitude': 0.0,
            'longitude': 0.0,
            'use_browser_location': False
        })
        # This should fail because 0.0 evaluates to False in Python
        self.assertFalse(form.is_valid())
    
    def test_save_location_with_coordinates(self):
        """Test saving location with coordinates"""
        form = LocationForm(data={
            'latitude': 1.2921,
            'longitude': 36.8219,
            'use_browser_location': True
        })
        self.assertTrue(form.is_valid())
        location = form.save_location()
        self.assertIsNotNone(location)
        self.assertEqual(location.latitude, 1.2921)
        self.assertEqual(location.longitude, 36.8219)
    
    def test_save_location_with_address_only(self):
        """Test saving location with address only"""
        form = LocationForm(data={
            'address': '123 Main Street',
            'use_browser_location': False
        })
        self.assertTrue(form.is_valid())
        location = form.save_location()
        self.assertIsNotNone(location)
        self.assertIsNone(location.latitude)
        self.assertIsNone(location.longitude)
    
    def test_get_or_create_location_with_same_coordinates(self):
        """Test that same coordinates return the same location object"""
        form1 = LocationForm(data={
            'latitude': 1.2921,
            'longitude': 36.8219,
            'use_browser_location': True
        })
        form1.is_valid()
        location1 = form1.save_location()
        
        form2 = LocationForm(data={
            'latitude': 1.2921,
            'longitude': 36.8219,
            'use_browser_location': True
        })
        form2.is_valid()
        location2 = form2.save_location()
        
        self.assertEqual(location1.id, location2.id)
        self.assertEqual(Location.objects.count(), 1)
