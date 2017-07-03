from django.contrib import admin
from .models import Binet, Mandat, TypeBinet

# définit les critères d'affichage dans l'interface admin

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


class TypeBinetAdmin(admin.ModelAdmin):
	list_display = ('nom',)





admin.site.register(Binet, BinetAdmin)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(TypeBinet, TypeBinetAdmin)