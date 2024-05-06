from pydoc import describe
from pyexpat import model
import tempfile
from django.conf import settings
from django.test import TestCase
from django.http import HttpRequest
from pandas import describe_option
from Photo.forms import BusinessPhotoAddForm,ProductPhotoAddForm
from Photo.models import ProductPhoto,BusinessPhoto
from Business.models import Business
from django.core.files.uploadedfile import SimpleUploadedFile


class TestForms(TestCase):
    def setUp(self):
        upload_file = open('media/test_image.jpg','rb')
        self.file_dict = {"photo":SimpleUploadedFile(upload_file.name,upload_file.read())}

    def test_BusinessPhotoAddForm_correct_data(self):
        form = BusinessPhotoAddForm({},self.file_dict)
        self.assertTrue(form.is_valid())

    def test_BusinessAddForm_wrong_data(self):
        form = BusinessPhotoAddForm({})
        self.assertFalse(form.is_valid())

    def test_ProductPhotoAddForm_correct_data(self):
        form = ProductPhotoAddForm({},self.file_dict)
        self.assertTrue(form.is_valid())

    def test_ProductPhotoAddForm_wrong_data(self):
        form = ProductPhotoAddForm(data={})
        self.assertFalse(form.is_valid())

 