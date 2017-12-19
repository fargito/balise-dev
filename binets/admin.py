from django.contrib import admin
from .models import Binet, Mandat, TypeBinet, TagBinet

# définit les critères d'affichage dans l'interface admin

class BinetAdmin(admin.ModelAdmin):
	list_display = ('nom', 'description', 'remarques_admins',)
	ordering = ('nom',)
	list_filter = ('tag_binet',)
	search_fields = ('nom',)


class MandatAdmin(admin.ModelAdmin):
	list_display = ('binet', 'promotion', 'president', 'tresorier', 'type_binet', 'is_active', 'description', 'remarques_admins')
	list_filter = ('promotion', 'type_binet', 'is_active', 'binet__tag_binet')
	ordering = ('binet', 'promotion')
	search_fields = ('binet__nom', 'promotion__nom', 'president__username', 'tresorier__username')


class TypeBinetAdmin(admin.ModelAdmin):
	list_display = ('nom',)

class TagBinetAdmin(admin.ModelAdmin):
	list_display = ('nom',)



admin.site.register(Binet, BinetAdmin)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(TypeBinet, TypeBinetAdmin)
admin.site.register(TagBinet, TagBinetAdmin)