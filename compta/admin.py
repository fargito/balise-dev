from django.contrib import admin
from .models import LigneCompta, PosteDepense

# enregistrement de la LigneCompta comme objet dans l'interface admin

class LigneComptaAdmin(admin.ModelAdmin):
	"""affiche de façon élégante les données dans l'interface admin"""
	list_display   = ('mandat', 'date', 'auteur', 'reference', 'description', 'debit', 'credit', 'is_locked', 'poste_depense')
	list_filter    = ('mandat', 'date', 'is_locked', 'poste_depense')
	date_hierarchy = 'date'
	ordering       = ('-date', )
	search_fields  = ('mandat', 'reference', 'debit', 'credit', 'poste_depense')

class PosteDepenseAdmin(admin.ModelAdmin):
	list_display =  ('nom', 'mandat',)
	list_filter  =  ('nom', 'mandat',)
	ordering     =  ('mandat', 'nom')
	search_fields = ('nom', 'mandat')

admin.site.register(LigneCompta, LigneComptaAdmin)
admin.site.register(PosteDepense, PosteDepenseAdmin)