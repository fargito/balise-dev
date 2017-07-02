from django.contrib import admin
from .models import Binet, Mandat, LigneCompta



class LigneComptaAdmin(admin.ModelAdmin):
	"""affiche de façon élégante les données dans l'interface admin"""
	list_display   = ('binet', 'date', 'auteur', 'description', 'debit', 'credit',)
	list_filter    = ('binet', 'date', 'debit', 'credit')
	date_hierarchy = 'date'
	ordering       = ('-date', )
	search_fields  = ('binet', 'debit', 'credit')



class BinetAdmin(admin.ModelAdmin):
	list_display = ('nom', 'current_promotion', 'current_president','current_tresorier', 'type_binet', 'is_active',
	 'description', 'remarques_admins',)
	list_filter = ('nom', 'is_active', 'type_binet', 'current_promotion')
	ordering = ('nom', 'current_promotion')
	search_fields = ('nom', 'current_president', 'current_tresorier')


class MandatAdmin(admin.ModelAdmin):
	list_display = ('binet', 'tresorier',)
	list_filter = ('binet', 'tresorier',)
	ordering = ('binet',)
	search_fields = ('binet', 'tresorier',)







admin.site.register(Binet, BinetAdmin)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(LigneCompta, LigneComptaAdmin)
