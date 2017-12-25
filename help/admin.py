from django.contrib import admin
from .models import HelpArticle

class HelpArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'subtitle', 'is_pdf', 'filename')
	ordering = ('title',)
	list_filter = ('is_pdf',)
	search_fields = ('nom', 'subtitle', 'filename')


admin.site.register(HelpArticle, HelpArticleAdmin)
