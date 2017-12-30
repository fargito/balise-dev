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
	poste_depense = models.ForeignKey('PosteDepense', null=True, blank=True)
	hidden_operation = models.ForeignKey('HiddenOperation', null=True, blank=True)

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
	def kick_self_link(self):
		"""retourne le lien vers la vue qui modifie cette ligne"""
		return ('kick_ligne', [self.id])

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

	@models.permalink
	def pass_to_next(self):
		"""passe la ligne au suivant"""
		return ('pass_ligne_to_next', [self.id])

	@models.permalink
	def pass_to_previous(self):
		"""passe la ligne au suivant"""
		return ('pass_ligne_to_previous', [self.id])

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

	def has_versed_deblocage(self):
		"""permet de savoir si des subventions on été versées sur la ligne"""
		deblocages_subvention = DeblocageSubvention.objects.filter(ligne_compta=self)
		none_versee = True
		for deblocage in deblocages_subvention:
			if deblocage.montant and deblocage.subvention.is_versee:
				none_versee = False
		return not(none_versee)



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

	@models.permalink
	def delete_self_url(self):
		"""retourne l'url de suppression de l'evenement"""
		return ('delete_evenement', [self.id])



class HiddenOperation(models.Model):
	"""permet de relier entre elles de façon uniquement accessible par les kessiers money des opérations.
	Permet notamment de faire les subventions banque.
	En gros permet de verser via un excel des opérations sur plusieurs binets"""
	title = models.CharField(max_length=30, verbose_name='Nom')
	add_date = models.DateTimeField(auto_now_add=True, auto_now=False,
								verbose_name="ajoutée le")
	close_date = models.DateTimeField(auto_now_add=False, auto_now=True,
								verbose_name="fermée le")
	creator = models.ForeignKey(User, verbose_name='ajoutée par', related_name='createur')
	closer = models.ForeignKey(User, verbose_name='fermée par', related_name='dernier_utilisateur')
	operation_type = models.ForeignKey('HiddenOperationType', verbose_name='Type')

	def __str__(self):
		return str(self.operation_type) + ' : ' + self.title

	class Meta:
		ordering = ('-close_date',)

	@models.permalink
	def operation_url(self):
		"""retourne la page de l'opération"""
		return ('operation_details', [self.id])

	@models.permalink
	def import_url(self):
		"""retourne la page pour importer des lignes sur l'opération"""
		return ('import_lignes_operation', [self.id])

	def get_totals(self):
		"""retourne la somme des dépenses et des recettes propres des lignes sur l'opération"""
		lignes = LigneCompta.objects.filter(hidden_operation=self)
		debit, credit = 0, 0
		for ligne in lignes:
			if ligne.debit:
				debit += ligne.debit
			if ligne.credit:
				credit += ligne.credit
		return debit, credit

	def get_lignes(self):
		"""retourne le queryset des lignes de l'opération """
		return LigneCompta.objects.filter(hidden_operation=self)


class HiddenOperationType(models.Model):
	"""sert à définir un type de HiddenOperation, comme par exemple remise de chèques ou subvention banque ou vague Polymédia
	Il y a possibilité de relier les HiddenOperationType à des postes de dépense génériques pour les ajouter en sous-main (cf Polymédia)"""
	nom = models.CharField(max_length=100)
	poste_depense = models.OneToOneField('PosteDepense', blank=True, null=True)

	def __str__(self):
		return self.nom