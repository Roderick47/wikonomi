import tempfile
from django.test import TestCase
from Business.forms import BusinessAddForm


class TestForms(TestCase):
    def test_BusinessAddForm_correct_data(self):
        form = BusinessAddForm({"name":"test_name",
        "location":"test_location",
        "description":"test_description",
        "image":tempfile.NamedTemporaryFile().name})
        self.assertTrue(form.is_valid())

    def test_BusinessAddForm_wrong_data(self):
        form = BusinessAddForm({"name":"",
        "location":"",
        "description":"",})
        self.assertFalse(form.is_valid())
