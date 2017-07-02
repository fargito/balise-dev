from django.contrib import admin
from .models import Eleve, Promotion



class PromotionAdmin(admin.ModelAdmin):
	ordering = ('-nom', )


class EleveAdmin(admin.ModelAdmin):
	list_display = ('nom', 'prenom', 'promotion',)
	list_filter = ('promotion', 'nom', 'prenom',)
	ordering = ('promotion', 'nom', 'prenom',)
	search_fields = ('promotion', 'nom', 'prenom',)


admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Eleve, EleveAdmin)