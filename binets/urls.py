from django.conf.urls import url
from django.views.generic import ListView

from . import views
from .models import Binet

urlpatterns = [
	url(r'^$', ListView.as_view(model=Binet, 
		template_name="binets/all_binets.html")),
]