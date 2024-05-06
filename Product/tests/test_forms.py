from unicodedata import name
from Product.forms import ProductAddForm,GetOrCreateBusinessForm
from django.test import TestCase
from Product.models import Product


class TestForms(TestCase):
    def test_ProductAddForm_correct_data(self):
        form = ProductAddForm({"name":"Test_product","price":20,"description":"Test_description"})
        self.assertTrue(form.is_valid())

    def test_ProductAddForm_wrong_data(self):
        form = ProductAddForm({"name":"","price":0,"description":""})
        self.assertFalse(form.is_valid())

    def test_GetOrCreateBusinessForm_correct_data(self):
        form = GetOrCreateBusinessForm({"business":"Test_business"})
        self.assertTrue(form.is_valid())

    def test_GetOrCreateBusinessForm_data(self):
        form = GetOrCreateBusinessForm({"business":""})
        self.assertFalse(form.is_valid())
