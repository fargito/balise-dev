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
	is_displayed = models.BooleanField(verbose_name = "Visible", default=True) # est affiché dans la liste des binets, accessible à tous
	being_checked = models.BooleanField(verbose_name = "Vérification compta commencée", default=False)
	president = models.ForeignKey(User, related_name = "president")
	tresorier = models.ForeignKey(User, related_name = "tresorier")
	promotion = models.ForeignKey('accounts.Promotion', verbose_name = "Promo")
	description = models.TextField(blank=True, null = True) # facultatif
	remarques_admins = models.TextField(blank=True, null = True) # facultatif
	
	create_date = models.DateTimeField(auto_now_add=True, auto_now=False,
								verbose_name="Date de création")
	passed_date = models.DateTimeField(default=None, null=True, blank=True, auto_now_add=False, auto_now=False,
								verbose_name="Date de passation")
	creator = models.ForeignKey(User)


	class Meta:
		unique_together = ('binet','promotion',)
		ordering = ('binet', 'promotion',)

	def __str__(self):
		return str(self.binet)+" ("+str(self.promotion)+")"

	@models.permalink
	def get_mandat_journal(self):
		"""returns the link to the mandat journal"""
		return ('mandat_journal', [self.id])

	@models.permalink
	def edit_self_url(self):
		"""link to the edit page"""
		return ('edit_mandat', [self.binet.id, self.id])

	@models.permalink
	def view_unview_self_url(self):
		"""return the link to the view where it goes from is_displayed to not is_displayed"""
		return ('mandat_view_unview', [self.id])

	@models.permalink
	def activate_deactivate_self_url(self):
		"""returns the link to the view that activates or deactivates this mandat"""
		return ('mandat_activate_deactivate', [self.id])

	@models.permalink
	def touch_untouch_self_url(self):
		return ('mandat_touch_untouch', [self.id])

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

	def is_all_locked(self):
		"""returns true if all the lines of this mandat have been checked"""
		return len(LigneCompta.objects.filter(mandat=self, is_locked=False)) == 0

	def has_next(self):
		"""returns true if a more recent mandat has been created"""
		return Mandat.objects.filter(binet=self.binet)[0] != self

	def get_status_verbose(self):
		"""used for the passation module : keyword used to describe the mandat's status"""
		if self.is_active:
			if self.being_checked:
				status = 'Vérification en cours'
			else:
				status = 'Compta non vérifiée'
		else:
			status = 'Compta vérifiée'
		if is_displayed:
			status += ', successeurs actifs'
		else:
			status += ', successeurs non actifs'
		return status

	def get_status(self):
		"""used for the passation module : keyword used to know the display color of the mandat"""
		if self.is_active:
			if self.being_checked:
				status = 'en-cours'
			else:
				status = 'non-touche'
		else:
			status = 'compta-verifiee'
		if self.is_displayed:
			status += '-successeurs-non-actifs'
		else:
			status += '-successeurs-actifs'
		return status

class Binet(models.Model):
	"""table dans la BDD représentant l'ensemble des binets"""
	nom = models.CharField(max_length=100)
	description = models.TextField(blank=True, null = True) # facultatif
	remarques_admins = models.TextField(blank=True, null = True) # facultatif

	create_date = models.DateTimeField(auto_now_add=True, auto_now=False,
								verbose_name="Date de création")
	creator = models.ForeignKey(User)


	
	class Meta:
		ordering = ('nom',)
		unique_together = ('nom',)

	def __str__(self):
		return self.nom

	@models.permalink
	def get_history_url(self):
		return ('binet_history', [self.id])

	@models.permalink
	def edit_self_url(self):
		return ('edit_binet', [self.id])

	@models.permalink
	def new_mandat_for_self_url(self):
		return ('new_mandat', [self.id])

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