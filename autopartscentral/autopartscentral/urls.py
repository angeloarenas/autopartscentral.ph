from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from views import IndexView
from views import LoginView

urlpatterns = [
    url(r"^$", IndexView.as_view(), name='index'),
    url(r"^account/login/", LoginView.as_view(), name='account_login'),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
