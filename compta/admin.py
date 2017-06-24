from django.contrib import admin
from .models import Binet, Promotion, Eleve, Mandat, LigneCompta



class LigneComptaAdmin(admin.ModelAdmin):
	"""affiche de façon élégante les données dans l'interface admin"""
	list_display   = ('binet', 'date', 'description', 'debit', 'credit', 'auteur')
	list_filter    = ('binet', 'date', 'debit', 'credit')
	date_hierarchy = 'date'
	ordering       = ('date', )
	search_fields  = ('binet', 'debit', 'credit')


class PromotionAdmin(admin.ModelAdmin):
	ordering = ('nom', )


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


class EleveAdmin(admin.ModelAdmin):
	list_display = ('nom', 'prenom', 'promotion',)
	list_filter = ('promotion', 'nom', 'prenom',)
	ordering = ('promotion', 'nom', 'prenom',)
	search_fields = ('promotion', 'nom', 'prenom',)



admin.site.register(Binet, BinetAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Eleve, EleveAdmin)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(LigneCompta, LigneComptaAdmin)
