from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import views

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name='index'),
    url(r"^account/login/", views.LoginView.as_view(), name='account_login'),
    url(r"^account/signup/", views.SignupView.as_view(), name='account_signup'),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
