from django.conf.urls import url
from django.views.generic import ListView

from . import views
from .models import Binet

urlpatterns = [
	url(r'^$', views.all_binets),
]