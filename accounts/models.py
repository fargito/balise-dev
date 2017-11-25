from django.db import models
# import pour avoir la base de donnees d'users
from django.contrib.auth.models import User
from binets.models import Mandat
from circuitdepart.models import ProblemDepart
from django.db.models import Q


class Promotion(models.Model):
	"""table des promotions"""
	nom = models.CharField(max_length=4)
	
	class Meta:
		ordering = ('-nom',)
		unique_together = ('nom',)

	def __str__(self):
		return self.nom

	@models.permalink
	def get_passations_url(self):
		"""returns the link to the passation details of this promotion"""
		return ('passation', [self.nom])

	@models.permalink
	def get_bilan_url(self):
		"""returns the link to the detailed bilan of this promotion"""
		return ('promo_bilan', [self.nom])

	@models.permalink
	def get_circuitdepart_url(self):
		"""returns the link to the circuitdepart page for the promotion"""
		return('circuitdepart', [self.nom])


class Eleve(models.Model):
	"""table des eleves. On la fait hériter de la table des users"""
	user = models.OneToOneField(User)
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	promotion = models.ForeignKey('Promotion')
	all_binets_passed = models.BooleanField(default=False)
	other_problem_circuitdepart = models.BooleanField(default=False)
	signed_fiche = models.BooleanField(default=False)

	class Meta:
		"""on définit ici les permissions pour le circuit de départ"""
		permissions = (
			("see_circuitdepart", "Voir le circuit de départ"),
			)

	def __str__(self):
		return "{0} {1} X{2}".format(self.prenom, self.nom, self.promotion)

	@models.permalink
	def get_infos_url(self):
		"""returns the url to view the personal infos of a student"""
		return ('view_account', [self.user.id])

	@models.permalink
	def sign_unsign_url(self):
		"""returns the link to sign the personnal fiche de départ of the eleve"""
		return ('fiche_sign_unsign', [self.id])

	def get_mandats(self):
		"""return the list of the mandats that the user owns"""
		if self.user.is_staff:
			return Mandat.objects.all()
		return Mandat.objects.filter(
			Q(president=self.user) | 
			Q(tresorier=self.user))

	def get_other_problems(self):
		"""returns the list of other problems the user has"""
		return ProblemDepart.objects.filter(user=self.user)

	def get_status(self):
		"""permet de retourner si l'utilisateur a fini ou non de passer ses binets"""
		if self.all_binets_passed and not(self.other_problem_circuitdepart):
			if self.signed_fiche:
				return "signed-fiche"
			else:
				return "no-problem"
		else:
			return "not-ready"

	def is_kessier(self):
		"""permet de savoir si l'utilisateur appartient au groupe 'kessiers perm'"""
		return self.has_perm('accounts.see_circuitdepart')