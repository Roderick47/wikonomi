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
from PIL import Image
import io


class TestForms(TestCase):
    def setUp(self):
        # Create a temporary test image in memory
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        
        self.file_dict = {"photo": SimpleUploadedFile(
            "test_image.jpg",
            image_file.read(),
            content_type="image/jpeg"
        )}

    def test_BusinessPhotoAddForm_correct_data(self):
        form = BusinessPhotoAddForm({},self.file_dict)
        self.assertTrue(form.is_valid())

    def test_BusinessAddForm_wrong_data(self):
        # Photo field is optional (blank=True, null=True), so form is valid without data
        form = BusinessPhotoAddForm({})
        self.assertTrue(form.is_valid())

    def test_ProductPhotoAddForm_correct_data(self):
        form = ProductPhotoAddForm({},self.file_dict)
        self.assertTrue(form.is_valid())

    def test_ProductPhotoAddForm_wrong_data(self):
        # Photo field is optional (blank=True, null=True), so form is valid without data
        form = ProductPhotoAddForm(data={})
        self.assertTrue(form.is_valid())

 