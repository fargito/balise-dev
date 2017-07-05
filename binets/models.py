from django.db import models
from django.contrib.auth.models import User

# stockage des binets avec leur type et les mandats
# qui les concernent

################################################
class TypeBinet(models.Model):
	"""types de binets
	ces types peuvent être
	avec chéquier, sans chéquier, ou compte exté"""
	nom = models.CharField(max_length=30)

	class Meta:
		unique_together = ('nom',)

	def __str__(self):
		return self.nom


class Mandat(models.Model):
	"""correspondance entre le binet et ses membres"""
	binet = models.ForeignKey('Binet')
	president = models.ForeignKey(User, related_name = "president")
	tresorier = models.ForeignKey(User, related_name = "tresorier")
	promotion = models.ForeignKey('accounts.Promotion', verbose_name = "Promo")

	class Meta:
		unique_together = ('binet','promotion',)

	def __str__(self):
		return str(self.id)



class Binet(models.Model):
	"""table dans la BDD représentant l'ensemble des binets"""
	nom = models.CharField(max_length=100)
	description = models.TextField(blank=True, null = True) # facultatif
	type_binet = models.ForeignKey('TypeBinet', verbose_name = "Type du binet")
	remarques_admins = models.TextField(blank=True, null = True) # facultatif
	is_active = models.BooleanField(verbose_name = "Actif", default=True)
	current_president = models.ForeignKey(User, verbose_name = "Président", related_name = "current_president")
	current_tresorier = models.ForeignKey(User, verbose_name = "Trésorier", related_name = "current_tresorier")
	current_promotion = models.ForeignKey('accounts.Promotion', verbose_name = "Promo")

	class Meta:
		ordering = ('current_promotion', 'nom',)
		unique_together = ('nom',)

	def __str__(self):
		return self.nom
