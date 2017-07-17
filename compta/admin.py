from django.contrib import admin
from .models import LigneCompta

# enregistrement de la LigneCompta comme objet dans l'interface admin

class LigneComptaAdmin(admin.ModelAdmin):
	"""affiche de façon élégante les données dans l'interface admin"""
	list_display   = ('mandat', 'date', 'auteur', 'description', 'debit', 'credit',)
	list_filter    = ('mandat', 'date', 'debit', 'credit')
	date_hierarchy = 'date'
	ordering       = ('-date', )
	search_fields  = ('mandat', 'debit', 'credit')

admin.site.register(LigneCompta, LigneComptaAdmin)