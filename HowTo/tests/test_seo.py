from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from Business.models import Business
from HowTo.models import HowTo
from Product.models import Product


class SeoIndexingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="seo-owner", email="seo@example.com", password="test-pass"
        )
        self.business = Business.objects.create(
            name="Test Shop", author=self.user, is_public=True
        )
        self.product = Product.objects.create(
            name="Fanta Orange 500ml",
            price=5.0,
            business=self.business,
            author=self.user,
            is_public=True,
        )
        self.guide = HowTo.objects.create(
            title="How to apply for a driving licence",
            description="PNG driving licence application guide",
            author=self.user,
            is_public=True,
        )

    def test_guide_history_is_noindex_and_canonicalizes_to_current_guide(self):
        response = self.client.get(
            reverse("HowTo:history", kwargs={"how_id": self.guide.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Robots-Tag"], "noindex, nofollow")
        self.assertContains(response, '<meta name="robots" content="noindex,nofollow">')
        self.assertContains(
            response,
            f'<link rel="canonical" href="http://testserver{self.guide_url}">',
        )

    def test_sitemap_includes_public_pages_but_not_history_pages(self):
        response = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"))
        body = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.guide_url, body)
        self.assertIn(reverse("Product:detail", kwargs={"prod_id": self.product.id}), body)
        self.assertIn(reverse("Business:detail", kwargs={"bus_id": self.business.id}), body)
        self.assertNotIn(
            reverse("HowTo:history", kwargs={"how_id": self.guide.id}), body
        )

    def test_robots_txt_advertises_sitemap(self):
        response = self.client.get(reverse("robots-txt"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")

    @property
    def guide_url(self):
        return reverse("HowTo:detail", kwargs={"how_id": self.guide.id})
