from django.db import models
# import pour avoir la base de donnees d'users
from django.contrib.auth.models import User
from binets.models import Mandat
from django.db.models import Q


class Promotion(models.Model):
	"""table des promotions"""
	nom = models.CharField(max_length=4)
	
	class Meta:
		ordering = ('-nom',)
		unique_together = ('nom',)

	def __str__(self):
		return self.nom


class Eleve(models.Model):
	"""table des eleves. On la fait hériter de la table des users"""
	user = models.OneToOneField(User)
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	promotion = models.ForeignKey('Promotion')

	def __str__(self):
		return "{0} {1} X{2}".format(self.prenom, self.nom, self.promotion)

	@models.permalink
	def get_infos_url(self):
		"""returns the url to view the personal infos of a student"""
		return ('view_account', [self.user.id])

	def get_mandats(self):
		"""return the list of the mandats that the user owns"""
		if self.user.is_staff:
			return Mandat.objects.all()
		return Mandat.objects.filter(
			Q(president=self.user) | 
			Q(tresorier=self.user))
