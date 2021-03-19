from django.urls import path
from .views import Webhook, Download

urlpatterns = [
    path("", Webhook),
    path("Download/", Download),
    ]
