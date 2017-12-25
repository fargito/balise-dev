from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.help_home, name='help_home'),
	url(r'^pdf/(?P<filename>[\w\_\-]+)$', views.open_file, name='view_pdf'),
	url(r'^article/(?P<article_id>\d+)$', views.help_article, name='help_article'),
	url(r'^article/add/$', views.add_article, name='add_article'),
	url(r'^article/add/pdf$', views.add_pdf_article, name='add_pdf_article'),
	url(r'^article/add/html$', views.add_html_article, name='add_html_article'),
	url(r'^article/delete/(?P<article_id>\d+)$', views.delete_article, name='delete_article'),
]