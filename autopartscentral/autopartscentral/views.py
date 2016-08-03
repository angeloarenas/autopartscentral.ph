from django.views.generic import TemplateView
import models
import account.views
import account.forms

class IndexView(TemplateView):
    template_name = "index.html"

    def product_featured(self):
        products = models.Product.objects.all()
        return products

class LoginView(account.views.LoginView):
    template_name = "login.html"
    form_class = account.forms.LoginEmailForm
