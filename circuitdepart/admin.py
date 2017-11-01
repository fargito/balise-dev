from django.contrib import admin
from .models import ProblemDepart


class ProblemDepartAdmin(admin.ModelAdmin):
	list_display = ('user', 'description', 'resolved',)
	list_filter = ('user', )
	ordering = ('user', 'description', 'resolved',)
	search_fields = ('user', 'description',)


admin.site.register(ProblemDepart, ProblemDepartAdmin)
