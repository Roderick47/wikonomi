import tempfile
from django.test import TestCase
from django.contrib.auth.models import User
from Business.models import Business

class TestModels(TestCase):
    def test_Businesss_Creation(self):
        test_user = User.objects.create(username="test_user",password="test_password")
        with tempfile.NamedTemporaryFile() as jpg:
            Business.objects.create(
                name ='Test_business',
                description="Test_description",
                location = "test_location",
                image= jpg.name,
                author = test_user,
                is_public=False)
        business = Business.objects.first()
        self.assertEqual(len(Business.objects.all()),1)
        self.assertTrue(isinstance(business,Business))
        self.assertEqual(business.name,'Test_business')
        self.assertEqual(business.location,"test_location")
        self.assertEqual(business.description,'Test_description')
        self.assertEqual(business.image,jpg.name)
        self.assertEqual(business.author,test_user)
        self.assertFalse(business.is_public)
    
