from os import remove
from django.test import TestCase, Client
from django.urls import reverse
from Photo.forms import ProductPhotoAddForm
from Product.forms import GetOrCreateBusinessForm, ProductAddForm
from Product.models import Product
from Business.models import Business
from django.contrib.auth.models import User
from urllib.parse import urlencode
import tempfile
import csv

class TestViews(TestCase):

    def setUp(self ):
        self.client = Client()
        self.test_business = Business.objects.create(
            name = 'test_business',
            description = 'business_description',
            location = 'business_location',
        )
        self.test_user = User.objects.create(username="test_user",password="test_password")
        self.test_product = Product.objects.create(
            name="test_product",
            price=10,
            description="test_description",
            business=self.test_business,
            )
        self.file=tempfile.NamedTemporaryFile()

    # Tests for ProductAddView
    def test_ProductAddView__GET__not_logged_in(self):
        url = reverse('Product:add',kwargs={"bus_id":1})
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertRedirects(response,redirect_url,302,200)

    def test_ProductAddView__GET__logged_in(self):
        url = reverse('Product:add',kwargs={"bus_id":1})
        self.client.force_login(self.test_user)
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Product/ProductAddForm.html')
        self.assertTrue(isinstance(response.context['form'],ProductAddForm))
        self.assertTrue(isinstance(response.context['imageForm'],ProductPhotoAddForm))
        self.assertTrue(isinstance(response.context['business'],Business))

    def test_ProductAddView__POST__no_data(self):
        url = reverse('Product:add',kwargs={"bus_id":1})
        self.client.force_login(self.test_user)
        response=self.client.post(url,{})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Product/ProductAddForm.html')
        self.assertTrue(isinstance(response.context['form'],ProductAddForm))
        self.assertTrue(isinstance(response.context['imageForm'],ProductPhotoAddForm))
        self.assertTrue(isinstance(response.context['business'],Business))

    def test_ProductAddView__POST__with_data(self):
        url = reverse('Product:add',kwargs={"bus_id":1})
        self.client.force_login(self.test_user)
        response=self.client.post(url,{
            "name":"test_product_edited",
            "price":50,
            "description":"description_edited"},
            {"photo":self.file.name}
            )
        redirect_url = reverse("Product:detail",kwargs={"prod_id":Product.objects.last().id})
        self.assertRedirects(response,redirect_url,302,200)
        self.assertEqual(len(Product.objects.all()),2)


    # Tests for ProductDetailView:
    # Authentication not needed for this view to render product details to user.
    def test_ProductDetailView__GET__not_Logged_in(self):
        url = reverse("Product:detail",kwargs={"prod_id":1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Product/ProductDetail.html')

    # Tests for ProductEditView:

    def test_ProductEditView__GET__not_logged_in(self):
        url = reverse("Product:edit",kwargs={"prod_id":1})
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response,redirect_url,302,200)

    def test_ProductEditView__GET__logged_in__wrong_Product_id(self):
        self.client.force_login(self.test_user)
        url = reverse("Product:edit",kwargs={"prod_id":100})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)

    def test_ProductEditView__GET__logged_in__right_Product_id(self):
        self.client.force_login(self.test_user)
        url = reverse("Product:edit",kwargs={"prod_id":self.test_product.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Product/ProductEditForm.html')
        self.assertTrue(isinstance(response.context['product'],Product))
        self.assertTrue(isinstance(response.context['form'],ProductAddForm))
        self.assertTrue(isinstance(response.context['imageForm'],ProductPhotoAddForm))

    def test_ProductEditView__POST__logged_in__right_product_id__no_data(self):
        self.client.force_login(self.test_user)
        url = reverse("Product:edit",kwargs={"prod_id":self.test_product.id})
        response = self.client.post(url,kwargs={})
        self.assertEquals(response.status_code,200)
        self.assertEquals(len(Product.objects.all()),1)
        self.assertTemplateUsed(response,'Product/ProductEditForm.html')
        self.assertTrue(isinstance(response.context['product'],Product))
        self.assertTrue(isinstance(response.context['form'],ProductAddForm))
        self.assertTrue(isinstance(response.context['imageForm'],ProductPhotoAddForm))

    def test_ProductEditView__POST__logged_in__right_product_id__with_data(self):
        self.client.force_login(self.test_user)
        url = reverse("Product:edit",kwargs={"prod_id":self.test_product.id})
        response = self.client.post(url,{
            "ProductAddForm":{
                "name":"test_product_edited",
                "price":50,
                "description":"description_edited"},
            "ProductPhotoAddForm":{"photo":self.file},
            }
            
            
            )
        self.assertEqual(len(Product.objects.all()),1)
        self.assertEqual(Product.objects.first().name,"test_product_edited")
        self.assertEquals(response.status_code,302)
        redirect_url = reverse("Product:detail",args=[Product.objects.first().id])
        self.assertRedirects(response,redirect_url,302,200)

    # Test for BusinessProductListView
    def test_BusinessProductListView__GET__not_logged_in(self):
        url = reverse("Product:business-list",kwargs={"bus_id":1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Product/BusinessProductGallery.html')
        self.assertTrue(isinstance(response.context['business'],Business))

    # Tests for  ProductAddGenerlView:
    def test_ProductAddGeneralView__GET__not_logged_in(self):
        url = reverse("Product:add-general")
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,redirect_url,302,200)

    def test_ProductAddGeneralView__POST__not_logged_in(self):
        url=reverse("Product:add-general")
        response = self.client.post(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response,redirect_url,302,200)

    def test_ProductAddGeneralView__GET__logged_in(self):
        url = reverse("Product:add-general")
        self.client.force_login(self.test_user)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'Product/GeneralProductAddForm.html')
        self.assertTrue(isinstance(response.context['form'],ProductAddForm))
        self.assertTrue(isinstance(response.context['form2'],GetOrCreateBusinessForm))
        self.assertTrue(isinstance(response.context['imageForm'],ProductPhotoAddForm))

    def test_ProductAddGeneralView__POST__logged_in__with_data(self):
        Business.objects.create(name="test_business",description="test_description")
        url = reverse("Product:add-general")
        self.client.force_login(self.test_user)
        response = self.client.post(url,{
            "name": "test_product_name",
            "price": 12,
            "business": "test_business"},
            {"image":self.file.name}
            )
        self.assertEquals(response.status_code, 302)
        self.assertEqual(len(Product.objects.all()),2)

    def test_ProductAddGeneralView__POST__logged_in__no_data(self):
        url = reverse("Product:add-general")
        self.client.force_login(self.test_user)
        response = self.client.post(url,kwargs={})
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(Product.objects.all()),1)
        self.assertEqual(len(Business.objects.all()),1)
        self.assertTemplateUsed(response,'Product/GeneralProductAddForm.html')
    
    # Tests for ProductDeleteView:
    def test_ProductDeleteView__GET__not_logged_in(self):
        url = reverse("Product:delete",kwargs={"prod_id":self.test_product.id})
        response = self.client.get(url)
        redirect_url= reverse("Product:detail",kwargs={"prod_id":self.test_product.id})
        self.assertRedirects(response,redirect_url,302,200)

    def test_ProductDeleteView__GET__logged_in(self):
        url = reverse("Product:delete",kwargs={"prod_id":self.test_product.id})
        self.client.force_login(self.test_user)
        response = self.client.get(url)
        self.assertEqual(len(Product.objects.all()),0)
        redirect_url= reverse("Home:home")
        self.assertRedirects(response,redirect_url,302,200)

    # Tests for ProductListTemplateDownload
    def test_ProductListTemplateDownload__GET__not_logged_in(self):
        url=reverse("Product:template-download")
        response = self.client.get(url)
        self.assertEquals(response.get('Content-Disposition'),"attachment; filename=product_list_template.csv")

    # Test ProductListUploadView
    def test_ProductListUploadView__GET__not_logged_in(self):
        url=reverse("Product:list-upload",kwargs={"bus_id":1})
        response = self.client.get(url)
        redirect_url = '{}?{}'.format(reverse("Profile:login"), urlencode({"next":url}))
        self.assertRedirects(response,redirect_url,302,200)
        
    def test_ProductListUploadView__GET__logged_in(self):
        url=reverse("Product:list-upload",kwargs={"bus_id":1})
        self.client.force_login(self.test_user)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'Product/import_product_list.html')

    def test_ProductListUploadView__POST__no_data(self):
        url=reverse("Product:list-upload",kwargs={"bus_id":1})
        self.client.force_login(self.test_user)
        response = self.client.post(url,kwargs={"myfile":""})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'Product/import_product_list.html')
        self.assertEqual(len(Product.objects.all()),1)

    def test_ProductListUploadView__POST__with_data(self):
        url=reverse("Product:list-upload",kwargs={"bus_id":1})
        self.client.force_login(self.test_user)
        file_name ="test.csv"
        with open(file_name,"w") as file:
            writer = csv.writer(file)
            writer.writerow(['name','price','description'])
            writer.writerow(['Test_Product2','12','test_description'])
            writer.writerow(['Test_Product3','30','3test_description'])
        with open(file_name,"rb") as file_data:
            response = self.client.post(url,{"bus_id":self.test_business.id,"myfile":file_data})
        redirect_url = reverse("Product:business-list",kwargs={"bus_id":self.test_business.id})
        self.assertRedirects(response,redirect_url,302,200)
        self.assertEqual(len(Product.objects.all()),3)
        remove(file_name)

    # def test_ProductAutoComplete(self):
    #     url = reverse("Product:autocomplete")
    #     response = self.client.get(url)

