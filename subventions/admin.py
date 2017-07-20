from django.contrib import admin
from .models import TypeSubvention, VagueSubventions, Subvention

class TypeSubventionAdmin(admin.ModelAdmin):
	"""affichage dans l'interface admin"""
	list_filter = ('nom',)
	search_fields = ('nom',)


class VagueSubventionsAdmin(admin.ModelAdmin):
	"""affichage dans l'interface admin"""
	list_display = ('type_subvention', 'annee',)
	list_filter = ('type_subvention', 'annee',)
	ordering = ('-annee',)
	search_fields = ('type_subvention', 'annee',)


class SubventionAdmin(admin.ModelAdmin):
	list_display = ('vague', 'mandat', 'demande', 'accorde', 'postes',)
	list_filter = ('vague', 'mandat', 'demande', 'accorde', 'postes',)
	ordering = ('vague', 'mandat',)
	search_fields = ('vague', 'mandat', 'demande', 'accorde', 'postes',)


admin.site.register(TypeSubvention, TypeSubventionAdmin)
admin.site.register(VagueSubventions, VagueSubventionsAdmin)
admin.site.register(Subvention, SubventionAdmin)