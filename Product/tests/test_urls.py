from django.test import SimpleTestCase
from django.urls import reverse,resolve
from Product.views import BusinessProductListView, ProductAddGeneralView,ProductAddView, ProductAutocomplete, ProductDeleteView, ProductDetailView,BusinessProductListView, ProductEditView, ProductListTemplateDownload, ProductListUpload


class TestUrls(SimpleTestCase):
    def test_add_general_url_resolves(self):
        url = reverse('Product:add-general')
        self.assertEquals(resolve(url).func, ProductAddGeneralView)

    def test_add_url_resolves(self):
        url = reverse('Product:add', kwargs={"bus_id":1})
        self.assertEquals(resolve(url).func, ProductAddView)

    def test_detail_url_resolves(self):
        url = reverse('Product:detail', kwargs={"prod_id":1})
        self.assertEquals(resolve(url).func, ProductDetailView)

    def test_business_list_url_resolves(self):
        url = reverse('Product:business-list', kwargs={"bus_id":1})
        self.assertEquals(resolve(url).func,BusinessProductListView)

    def test_edit_url_resolves(self):
        url = reverse('Product:edit', kwargs={"prod_id":1})
        self.assertEquals(resolve(url).func,ProductEditView)

    def test_delete_url_resolves(self):
        url = reverse('Product:delete', kwargs={"prod_id":1})
        self.assertEquals(resolve(url).func,ProductDeleteView)
    
    def test_autocomplete_url_resolves(self):
        url = reverse('Product:autocomplete')
        self.assertEquals(resolve(url).func,ProductAutocomplete)

    def test_list_upload_url_resolves(self):
        url = reverse('Product:list-upload', kwargs={"bus_id":1})
        self.assertEquals(resolve(url).func,ProductListUpload)

    def test_template_download_url_resolves(self):
        url = reverse('Product:template-download')
        self.assertEquals(resolve(url).func,ProductListTemplateDownload)

    

    

    
        

    
        