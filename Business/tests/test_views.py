from os import remove
from django.test import TestCase, Client
from django.urls import reverse
from Business.forms import BusinessAddForm
from Product.models import Product

from Business.models import Business
from django.contrib.auth.models import User
from urllib.parse import urlencode
import tempfile
import csv
from django.db.models.query import QuerySet


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_business = Business.objects.create(
            name = 'test_business',
            description = 'business_description',
            location = 'business_location',
        )
        self.test_user = User.objects.create(username="test_user",password="test_password")
        self.test_product = Product.objects.create(
            name="test_product",
            price=10,description="test_description",
            business=self.test_business,
            )
        self.file = tempfile.NamedTemporaryFile()

    # Tests for ProductAddView
    def test_BusinessAddView__GET__not_logged_in(self):
        url = reverse('Business:add')
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertRedirects(response,redirect_url,302,200)

    # Tests for BusinessAddView
    def test_BusinessAddView__GET__logged_in(self):
        self.client.force_login(self.test_user)
        url = reverse('Business:add')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/BusinessAddForm.html')
        self.assertTrue(isinstance(response.context['form'],BusinessAddForm ))

    def test_BusinessAddView__POST__not_logged_in(self):
        url = reverse("Business:add")
        response = self.client.post(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertRedirects(response,redirect_url,302,200)

    def test_BusinessAddView__POST__with_wrong_data(self):
        form=BusinessAddForm
        self.client.force_login(self.test_user)
        url = reverse("Business:add")
        response = self.client.post(url,kwargs={})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/BusinessAddForm.html')
        self.assertEqual(len(Business.objects.all()),1)
        self.assertTrue(isinstance(response.context['form'],BusinessAddForm))

    def test_BusinessAddView__POST__with_correct_data(self):
        url = reverse("Business:add")
        self.client.force_login(self.test_user)
        response = self.client.post(url,{
            'name':'test_business', 
            'description':'test_description',
            'location':'test_location',
            'image':self.file.name,
            'author':self.test_user,
        })
        new_business= Business.objects.last()
        self.assertEqual(len(Business.objects.all()),2)
        self.assertEqual(new_business.name,'test_business')
        redirect_url = reverse("Business:detail",kwargs={"bus_id":new_business.id})
        self.assertRedirects(response,redirect_url,302,200)

    # Tests for BusinessEditView
    def test_BusinessEditView_GET_not_logged_in(self):
        url = reverse("Business:edit",kwargs={"bus_id":self.test_business.id})
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertRedirects(response,redirect_url,302,200)

    def test_BusinessEditView_GET_logged_in(self):
        url = reverse("Business:edit",kwargs={"bus_id":self.test_business.id})
        self.client.force_login(self.test_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/BusinessEditForm.html')
        self.assertTrue(isinstance(response.context['form'],BusinessAddForm))
        self.assertTrue(isinstance(response.context['business'],Business))
        

    def test_BusinessEditView__POST__no_data(self):
        url = reverse("Business:edit",kwargs={"bus_id":self.test_business.id})
        self.client.force_login(self.test_user)
        response = self.client.get(url,{})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/BusinessEditForm.html')
        self.assertTrue(isinstance(response.context['form'],BusinessAddForm))
        self.assertTrue(isinstance(response.context['business'],Business))

    def test_BusinessEditView__POST__with_data(self):
        url = reverse("Business:edit",kwargs={"bus_id":self.test_business.id})
        self.client.force_login(self.test_user)
        response = self.client.post(url,{
            'name':'test_business_edit', 
            'description':'test_description',
            'location':'test_location',
            'image':self.file.name,
            'author':self.test_user,
        })
        self.assertEqual(len(Business.objects.all()),1)
        business=Business.objects.get(id=1) 
        self.assertEqual(business.name,'test_business_edit')
        redirect_url = reverse("Business:detail",kwargs={"bus_id":self.test_business.id})
        self.assertRedirects(response,redirect_url,302,200)

    # Test for BusinessDetailView
    def test_BusinessDetailView__GET(self):
        url = reverse('Business:detail',kwargs={"bus_id":self.test_business.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/BusinessDetail.html')
        self.assertTrue(isinstance(response.context['business'],Business))
        self.assertTrue(isinstance(response.context['products'],QuerySet))


    # Tests for PrivateBusinessAddView
    def test_PrivateBusinessAddView__GET__not_logged_in(self):
        url = reverse('Business:add-private')
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertRedirects(response,redirect_url,302,200)

    def test_PrivateBusinessAddView__GET__logged_in(self):
        url = reverse('Business:add-private')
        self.client.force_login(self.test_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/PrivateBusinessAddForm.html')
        self.assertTrue(isinstance(response.context['form'],BusinessAddForm))

    def test_PrivateBusinessAddView__POST__no_data(self):
        url = reverse('Business:add-private')
        self.client.force_login(self.test_user)
        response = self.client.post(url,{})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'Business/PrivateBusinessAddForm.html')
        self.assertTrue(isinstance(response.context['form'],BusinessAddForm))

    def test_PrivateBusinessAddView__POST__with_data(self):
        url = reverse('Business:add-private')
        self.client.force_login(self.test_user)
        response = self.client.post(url,{
            'name':'private_business',
            'description':'private_business_description',
            'location':"private_business_location",
            'image':tempfile.NamedTemporaryFile().name,
        })
        new_business = Business.objects.last()
        redirect_url = reverse("Home:home")
        self.assertRedirects(response,redirect_url,302,200)
        self.assertEqual(len(Business.objects.all()),2)
        self.assertEqual(new_business.name,'private_business')
    
    # Tests for AllBusinessListView
    def test_AllBusinessListView__GET(self):
        url = reverse('Business:all')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'Business/allBusiness.html')
        self.assertIsInstance(response.context['all_business'],QuerySet)

