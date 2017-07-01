from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.home),
    url(r'^article/(\d+)$', views.view_article),
]
