from django.test import SimpleTestCase
from django.urls import reverse,resolve
from Business.views import BusinessAddView,BusinessEditView,BusinessDetailView,PrivateBusinessAddView,AllBusinessListView

class TestUrls(SimpleTestCase):
    def test_detail_url_resolves(self):
        url = reverse('Business:detail',kwargs={"bus_id":1})
        self.assertEquals(resolve(url).func, BusinessDetailView)

    def test_add_general_url_resolves(self):
        url = reverse('Business:add')
        self.assertEquals(resolve(url).func, BusinessAddView)

    def test_add_private_url_resolves(self):
        url = reverse('Business:add-private')
        self.assertEquals(resolve(url).func, PrivateBusinessAddView)

    def test_edit_url_resolves(self):
        url = reverse('Business:edit', kwargs={"bus_id":1})
        self.assertEquals(resolve(url).func, BusinessEditView)

    def test_all_url_resolves(self):
        url = reverse('Business:all')
        self.assertEquals(resolve(url).func, AllBusinessListView)

    

    
        

    
        