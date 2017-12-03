from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from subventions.models import Subvention, DeblocageSubvention


class LigneCompta(models.Model):
	"""opérations comptables Elles sont liées à la fois à
	un binet pour que ce soit facile à éditer et à un 
	Mandat pour l'historique"""
	mandat = models.ForeignKey('binets.Mandat')
	date = models.DateField(auto_now_add=False, auto_now=False, 
                                verbose_name="Effectuée le")
	add_date = models.DateTimeField(auto_now_add=True, auto_now=False,
								verbose_name="ajoutée le")
	edit_date = models.DateTimeField(auto_now_add=False, auto_now=True,
								verbose_name="modifiée le")
	auteur = models.ForeignKey(User, verbose_name = 'ajoutée par', related_name="auteur")
	modificateur = models.ForeignKey(User, verbose_name = 'modifiée par', related_name="modificateur")
	description = models.CharField(max_length=100)
	commentaire = models.TextField(blank=True, null=True)
	reference = models.CharField(max_length=15, null=True, blank=True)
	debit = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=2)
	credit = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=2)
	is_locked = models.BooleanField(default=False)
	facture_ok = models.BooleanField(default=False)
	poste_depense = models.ForeignKey('PosteDepense', null=True)

	def __str__(self):
		return self.description

	class Meta:
		ordering = ('-date', '-reference','-id')
		permissions = (
			("validate_polymedia", "Effectuer des validations Polymédia"),
			)

	@models.permalink
	def delete_self_link(self):
		"""retourne le lien vers la vue qui supprime la ligne"""
		return ('delete_ligne', [self.id])

	@models.permalink
	def edit_self_link(self):
		"""retourne le lien vers la vue qui modifie cette ligne"""
		return ('edit_ligne', [self.id])

	@models.permalink
	def view_self_link(self):
		"""retourne le lien vers la vue qui modifie cette ligne"""
		return ('view_ligne', [self.id])

	@models.permalink
	def lock_unlock_self_link(self):
		"""permet de passer is_locked à sa valeur contraire"""
		return ('lock_unlock_ligne', [self.id])

	@models.permalink
	def check_uncheck_self_link(self):
		"""permet de passer is_locked à sa valeur contraire"""
		return ('check_uncheck_ligne', [self.id])

	@models.permalink
	def lock_unlock_self_polymedia_link(self):
		"""permet de passer is_locked à sa valeur contraire"""
		return ('lock_unlock_ligne_polymedia', [self.id])


	def get_deblocages(self):
		"""retourne une liste de querysets contenant les déblocages effectués sur les différentes
		vagues attribuées au mandat"""
		mandat_subventions = Subvention.objects.filter(mandat=self.mandat)
		ligne_deblocages = []
		for subvention in mandat_subventions:
			deblocage = DeblocageSubvention.objects.filter(
				subvention=subvention, ligne_compta=self)
			if len(deblocage) == 0:
				new_deblocage = DeblocageSubvention.objects.create(
					ligne_compta=self,
					subvention=subvention,
					montant=None)
				new_deblocage.save()
				ligne_deblocages.append((subvention, None))
			else:
				ligne_deblocages.append((subvention, deblocage[0].montant))
		return ligne_deblocages


	def get_deblocages_for_formset(self):
		"""retourne une liste de dict du type [{ 'montant': 159.99}, ] pour la mise en decimal_places
		initiale du formset de déblocage dans la modification de ligne"""
		mandat_subventions = Subvention.objects.filter(mandat=self.mandat)
		ligne_deblocages = []
		for subvention in mandat_subventions:
			deblocage = DeblocageSubvention.objects.filter(
				subvention=subvention, ligne_compta=self)
			if len(deblocage) == 0:
				new_deblocage = DeblocageSubvention.objects.create(
					ligne_compta=self,
					subvention=subvention,
					montant=None)
				new_deblocage.save()
				ligne_deblocages.append({'montant': None})
			else:
				ligne_deblocages.append({'montant': deblocage[0].montant})
		return ligne_deblocages



class PosteDepense(models.Model):
	"""definit un poste de dépense. Ces postes sont associés à des mandats, pour éviter que chaque mandat
	se retrouve avec les postes de tout le monde.
	Les postes qui ont un mandat None sont attribués à tout le monde.
	C'est le cas de Polymédia par exemple"""

	nom = models.CharField(max_length=15)
	mandat = models.ForeignKey('binets.Mandat', null=True, blank=True)
	evenement = models.ForeignKey('Evenement', null=True, blank=True)
	previsionnel_debit = models.DecimalField(default=0, max_digits=9, decimal_places=2)
	previsionnel_credit = models.DecimalField(default=0, max_digits=9, decimal_places=2)

	def __str__(self):
		if self.evenement:
			return self.evenement.code + '/' + self.nom
		else:
			return self.nom

	class Meta:
		ordering = ('evenement', 'nom',)
		unique_together = ('nom', 'evenement', 'mandat',)


	def get_default_index(self):
		"""pour ligne_edit, retourne le rang du choix par défault de"""
		return PosteDepense.objects.filter(
				Q(mandat=self.mandat) | Q(mandat=None)).filter(nom__lt=self.nom).count()

	@models.permalink
	def edit_self_url(self):
		"""retourne l'url de modification du poste de dépense"""
		return ('edit_poste_depense', [self.id])

	@models.permalink
	def delete_self_url(self):
		"""retourne l'url de destruction du poste de dépense"""
		return ('delete_poste_depense', [self.id])



class Evenement(models.Model):
	"""definit un evenement, c'est-à-dire un regroupement de postes de dépenses.
	Comme les postes de dépenses, ces événements sont associés à des mandats, pour éviter que chaque mandat
	se retrouve avec les postes de tout le monde.
	Les postes qui ont un evenement None sont mis dans un événement par défaut du binet"""

	nom = models.CharField(max_length=15)
	code = models.CharField(max_length=3)
	mandat = models.ForeignKey('binets.Mandat')

	def __str__(self):
		return self.nom

	class Meta:
		ordering = ('nom',)
		unique_together = ('nom', 'code', 'mandat',)

	@models.permalink
	def edit_self_url(self):
		"""retourne l'url de modification de l'evenement"""
		return ('edit_evenement', [self.id])