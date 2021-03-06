from django.contrib import admin
from django.urls import path, include
from Home.views import HomePage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("Download/", include("Home.urls")),
    path("", HomePage),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
