from django.contrib import admin
from .models import TypeSubvention, VagueSubventions, Subvention

class TypeSubventionAdmin(admin.ModelAdmin):
	"""affichage dans l'interface admin"""
	search_fields = ('nom',)


class VagueSubventionsAdmin(admin.ModelAdmin):
	"""affichage dans l'interface admin"""
	list_display = ('type_subvention', 'annee',)
	list_filter = ('type_subvention', 'annee',)
	ordering = ('-annee',)
	search_fields = ('type_subvention__nom', 'annee',)


class SubventionAdmin(admin.ModelAdmin):
	list_display = ('vague', 'mandat', 'demande', 'accorde', 'postes',)
	list_filter = ('vague__annee', 'vague__type_subvention', 'mandat__promotion', 'mandat__binet',)
	ordering = ('vague', 'mandat',)
	search_fields = ('vague__type_subvention__nom', 'mandat__binet__nom', 'demande', 'accorde', 'postes',)


admin.site.register(TypeSubvention, TypeSubventionAdmin)
admin.site.register(VagueSubventions, VagueSubventionsAdmin)
admin.site.register(Subvention, SubventionAdmin)