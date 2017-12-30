from django.contrib import admin
from .models import LigneCompta, PosteDepense, Evenement, HiddenOperation, HiddenOperationType

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
	list_display  = ('title', 'operation_type', 'add_date', 'close_date')
	list_filter   = ('close_date',)
	ordering      = ('-close_date',)
	search_fields = ('title', 'operation_type')

class HiddenOperationTypeAdmin(admin.ModelAdmin):
	list_display = ('nom', 'poste_depense')
	ordering     = ('nom',)
	search_fields = ('nom', 'poste_depense')

admin.site.register(LigneCompta, LigneComptaAdmin)
admin.site.register(PosteDepense, PosteDepenseAdmin)
admin.site.register(Evenement, EvenementAdmin)
admin.site.register(HiddenOperation, HiddenOperationAdmin)
admin.site.register(HiddenOperationType, HiddenOperationTypeAdmin)