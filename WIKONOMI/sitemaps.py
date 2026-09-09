from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from Business.models import Business
from HowTo.models import HowTo
from Product.models import Product


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return ["Home:home", "Product:all", "Business:all", "HowTo:list"]

    def location(self, item):
        return reverse(item)


class GuideSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return HowTo.objects.filter(is_public=True).order_by("id")

    def location(self, obj):
        return reverse("HowTo:detail", kwargs={"how_id": obj.id})

    def lastmod(self, obj):
        return obj.updated_at


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(
            is_public=True, business__is_public=True
        ).order_by("id")

    def location(self, obj):
        return reverse("Product:detail", kwargs={"prod_id": obj.id})

    def lastmod(self, obj):
        return obj.date_updated


class BusinessSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Business.objects.filter(is_public=True).order_by("id")

    def location(self, obj):
        return reverse("Business:detail", kwargs={"bus_id": obj.id})

    def lastmod(self, obj):
        return obj.date_updated


sitemaps = {
    "static": StaticViewSitemap,
    "guides": GuideSitemap,
    "products": ProductSitemap,
    "businesses": BusinessSitemap,
}
