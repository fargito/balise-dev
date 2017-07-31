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
	is_active = models.BooleanField(verbose_name = "Actif", default=True)
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
		if self.is_active:
			# is_active est défini pour tous les binets par défaut sur True
			# lorsque la compta a été vérifiée, elle passe à false et les membres ne peuvent plus modifier
			# les admins peuvent toujours
			authorized['edit'].append(self.president)
			authorized['edit'].append(self.tresorier)
		return authorized


class Binet(models.Model):
	"""table dans la BDD représentant l'ensemble des binets"""
	nom = models.CharField(max_length=100)
	description = models.TextField(blank=True, null = True) # facultatif
	remarques_admins = models.TextField(blank=True, null = True) # facultatif

	
	class Meta:
		ordering = ('nom',)
		unique_together = ('nom',)

	def __str__(self):
		return self.nom

	@models.permalink
	def get_history_url(self):
		return ('binet_history', [self.id])

	def get_available_mandats(self, user):
		"""retourne la liste des mandats auquel l'utilisateur a accès"""
		if user.is_staff:
			return Mandat.objects.filter(binet=self)
		
		return Mandat.objects.filter(
			binet=self,
			promotion__lte=user.eleve.promotion)

	def get_latest_mandat(self):
		"""returns the last mandat"""
		return Mandat.objects.filter(binet=self)[0]