from django.db import models
from django.contrib.auth.models import User
from compta.models import LigneCompta
from django.db.models import Q
from subventions.models import Subvention

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
	type_binet = models.ForeignKey('TypeBinet', verbose_name = "Type du binet")
	president = models.ForeignKey(User, related_name = "president")
	tresorier = models.ForeignKey(User, related_name = "tresorier")
	promotion = models.ForeignKey('accounts.Promotion', verbose_name = "Promo")
	description = models.TextField(blank=True, null = True) # facultatif
	remarques_admins = models.TextField(blank=True, null = True) # facultatif


	class Meta:
		unique_together = ('binet','promotion',)
		ordering = ('binet', 'promotion',)

	def __str__(self):
		return str(self.binet)+" ("+str(self.promotion)+")"

	@models.permalink
	def get_mandat_journal(self):
		"""returns the link to the mandat journal"""
		return ('mandat_journal', [self.id])

	def get_subtotals(self):
		"""returns the total credits and debits attached
		to this mandat without the subventions"""
		lignes = LigneCompta.objects.filter(mandat=self)
		debit_subtotal = 0
		credit_subtotal = 0
		for ligne in lignes:
			if ligne.credit:
				credit_subtotal += ligne.credit
			if ligne.debit:
				debit_subtotal += ligne.debit
		return (debit_subtotal, credit_subtotal)

	def get_totals(self):
		"""returns the totals with the subventions"""
		subventions = Subvention.objects.filter(mandat=self)
		debit_total, credit_total = self.get_subtotals()
		for subvention in subventions:
			credit_total += subvention.get_deblocages_total()
		return (debit_total, credit_total)


	def get_balance(self):
		"""retourne la balance actuelle du binet"""
		debit, credit = self.get_totals()
		return credit-debit

	def is_current(self):
		"""returns if the mandat is currently the last"""
		return self.promotion == self.binet.current_promotion

	def get_authorized_users(self):
		"""returns a dict of edit and view users. 
		They are the users from the future mandats
		If the mandat is current, then the owners of this mandat can
		edit its compta. If not, they can just view it"""
		future_mandats = Mandat.objects.filter(
			binet=self.binet, promotion__gt=self.promotion)
		authorized = {'edit':[], 'view':[]}
		for future_mandat in future_mandats:
			authorized['view'].append(future_mandat.president)
			authorized['view'].append(future_mandat.tresorier)
		authorized['view'].append(self.president)
		authorized['view'].append(self.tresorier)
		if self.is_current():
			# actuellement le seul critère pour savoir si les membres
			# d'un binet peuvent éditer leur compta est qu'ils n'aient pas
			# de successeurs. A changer avec le  module passation ?
			authorized['edit'].append(self.president)
			authorized['edit'].append(self.tresorier)
		return authorized


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

	@models.permalink
	def get_history_url(self):
		return ('binet_history', [self.id])

	class Meta:
		ordering = ('current_promotion', 'nom',)
		unique_together = ('nom',)

	def __str__(self):
		return self.nom

	def get_available_mandats(self, user):
		"""retourne la liste des mandats auquel l'utilisateur a accès"""
		if user.is_staff:
			res = {
				'edit': Mandat.objects.filter(binet=self),
			}
			return res
		res = {}
		res['view'] = Mandat.objects.filter(
			binet=self,
			promotion__lt=user.eleve.promotion)
		res['edit'] = Mandat.objects.filter(binet=self).filter(
			Q(president=user) | 
			Q(tresorier=user))
		return res