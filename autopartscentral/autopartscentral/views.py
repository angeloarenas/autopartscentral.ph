from django.views.generic import TemplateView
from models import ProductFeatured
from models import Product

class IndexView(TemplateView):
    template_name = "index_show.html"

    def product_featured(self):
        products = Product.objects.all()
        #products.productfeatured_set.all()
        return products
