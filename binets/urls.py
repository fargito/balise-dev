from django.conf.urls import url
from django.views.generic import ListView

from . import views
from .models import Binet

urlpatterns = [
	url(r'^$', views.all_binets),
	url(r"^history/(?P<id_binet>\d+)$", views.binet_history, name='binet_history'),
]