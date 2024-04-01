from Business.models import Business
from Product.models import Product
from django.test import TestCase
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.test_business = Business.objects.create(
            name = 'test_business',
            description = 'business_description',
            location = 'business_location',
        )
        self.test_user = User.objects.create(username="test_user",password="test_password")

    def test_Product_Creation(self):
        Product.objects.create(
            name ='Test_name',
            price = 200, 
            description="Test_description",
            business=self.test_business,
            author = self.test_user)
        product = Product.objects.first()
        self.assertEqual(len(Product.objects.all()),1)
        self.assertTrue(isinstance(product,Product))
        self.assertEqual(product.name,'Test_name')
        self.assertEqual(product.price,200)
        self.assertEqual(product.description,'Test_description')
        self.assertEqual(product.business,self.test_business)
        self.assertEqual(product.author,self.test_user)



