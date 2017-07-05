from django.db import models
# import pour avoir la base de donnees d'users
from django.contrib.auth.models import User


class Promotion(models.Model):
	"""table des promotions"""
	nom = models.CharField(max_length=4)
	
	class Meta:
		ordering = ('-nom',)

	def __str__(self):
		return self.nom


class Eleve(models.Model):
	"""table des eleves. On la fait hériter de la table des users"""
	user = models.OneToOneField(User)
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	promotion = models.ForeignKey('Promotion')

	def __str__(self):
		return "{0} {1} X{2}".format(self.nom, self.prenom, self.promotion)