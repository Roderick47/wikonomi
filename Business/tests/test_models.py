import tempfile
from django.test import TestCase
from django.contrib.auth.models import User
from Business.models import Business
from Location.models import Location

class TestModels(TestCase):
    def setUp(self):
        # Create test user
        self.test_user = User.objects.create_user(
            username="test_user",
            password="test_password"
        )
        # Create test location
        self.test_location = Location.objects.create(
            latitude=0.0,
            longitude=0.0
        )
        
    def test_Business_Creation(self):
        with tempfile.NamedTemporaryFile() as jpg:
            business = Business.objects.create(
                name='Test_business',
                description="Test_description",
                location=self.test_location,
                image=jpg.name,
                author=self.test_user,
                is_public=False
            )
            
        # Verify the business was created correctly
        self.assertEqual(Business.objects.count(), 1)
        self.assertIsInstance(business, Business)
        self.assertEqual(business.name, 'Test_business')
        self.assertEqual(business.location, self.test_location)
        self.assertEqual(business.description, 'Test_description')
        self.assertEqual(business.image, jpg.name)
        self.assertEqual(business.author, self.test_user)
        self.assertFalse(business.is_public)
    
