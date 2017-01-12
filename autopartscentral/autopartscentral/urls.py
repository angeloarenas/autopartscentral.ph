from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import views

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name='index'),
    url(r"^account/login/$", views.LoginView.as_view(), name='account_login'),
    url(r"^account/signup/$", views.SignupView.as_view(), name='account_signup'),
    url(r"^account/dashboard/$", views.AccountDashboardView.as_view(), name='account_dashboard'),
    url(r"^account/profile/$", views.AccountProfileView.as_view(), name='account_profile'),
    url(r"^account/addresses/$", views.AccountAddressesView.as_view(), name='account_addresses'),
    url(r"^account/orders/$", views.AccountOrdersView.as_view(), name='account_orders'),
    url(r"^account/orders/detail/$", views.AccountOrdersView.as_view(), name='account_orders_detail'),

    url(r"^shop/$", views.ShopView.as_view(), name='shop'),
    url(r"^shop/detail/$", views.ShopDetailView.as_view(), name='shop_detail'),

    url(r"^cart/$", views.CartView.as_view(), name='cart'),
    url(r"^checkout/step/login/$", views.CheckoutLoginView.as_view(), name='checkout_login'),
    url(r"^checkout/step/shipping/$", views.CheckoutShippingView.as_view(), name='checkout_shipping'),
    url(r"^checkout/step/review/$", views.CheckoutReviewView.as_view(), name='checkout_review'),
    url(r"^checkout/step/complete/$", views.CheckoutCompleteView.as_view(), name='checkout_complete'),

    url(r"^cart/add/$", views.cart_add, name='cart_add'),
    url(r"^cart/remove/$", views.cart_remove, name='cart_remove'),
    url(r"^cart/update/$", views.cart_update, name='cart_update'),
    url(r"^vehicle/filter/$", views.vehicle_filter, name='vehicle_filter'),

    url(r"^admin/", include(admin.site.urls)),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
