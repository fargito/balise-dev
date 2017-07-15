from django.contrib import admin
from .models import LigneCompta, TypeSubvention, VagueSubventions, Subvention

# enregistrement de la LigneCompta comme objet dans l'interface admin

class LigneComptaAdmin(admin.ModelAdmin):
	"""affiche de façon élégante les données dans l'interface admin"""
	list_display   = ('mandat', 'date', 'auteur', 'description', 'debit', 'credit',)
	list_filter    = ('mandat', 'date', 'debit', 'credit')
	date_hierarchy = 'date'
	ordering       = ('-date', )
	search_fields  = ('mandat', 'debit', 'credit')


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



admin.site.register(LigneCompta, LigneComptaAdmin)
admin.site.register(TypeSubvention, TypeSubventionAdmin)
admin.site.register(VagueSubventions, VagueSubventionsAdmin)
admin.site.register(Subvention, SubventionAdmin)