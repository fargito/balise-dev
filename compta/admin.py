from django.contrib import admin
from .models import LigneCompta, PosteDepense, Evenement, HiddenOperation

# enregistrement de la LigneCompta comme objet dans l'interface admin

class LigneComptaAdmin(admin.ModelAdmin):
	"""affiche de façon élégante les données dans l'interface admin"""
	list_display   = ('mandat', 'date', 'auteur', 'reference', 'description', 'debit', 'credit', 'is_locked', 'poste_depense')
	list_filter    = ('date', 'is_locked', 'mandat__promotion', 'mandat__binet')
	date_hierarchy = 'date'
	ordering       = ('-date', )
	search_fields  = ('mandat__binet__nom', 'reference', 'debit', 'credit', 'poste_depense__nom')

class PosteDepenseAdmin(admin.ModelAdmin):
	list_display =  ('nom', 'mandat', 'evenement')
	list_filter  =  ('mandat__promotion', 'mandat__binet')
	ordering     =  ('mandat', 'nom')
	search_fields = ('nom', 'mandat')

class EvenementAdmin(admin.ModelAdmin):
	list_display =  ('nom', 'mandat', 'code',)
	list_filter  =  ('mandat__promotion', 'mandat__binet')
	ordering     =  ('mandat', 'nom')
	search_fields = ('nom', 'mandat')

class HiddenOperationAdmin(admin.ModelAdmin):
	list_display  = ('title', 'date')
	list_filter   = ('date',)
	ordering      = ('-date',)
	search_fields = ('title',)

admin.site.register(LigneCompta, LigneComptaAdmin)
admin.site.register(PosteDepense, PosteDepenseAdmin)
admin.site.register(Evenement, EvenementAdmin)
admin.site.register(HiddenOperation, HiddenOperationAdmin)