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
	debit = models.DecimalField(null=True, blank=True,max_digits=9, decimal_places=2)
	credit = models.DecimalField(null=True, blank=True,max_digits=9, decimal_places=2)
	is_locked = models.BooleanField(default=False)
	poste_depense = models.ForeignKey('PosteDepense', null=True)

	def __str__(self):
		return self.description

	class Meta:
		ordering = ('-date','-id')

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
				ligne_deblocages.append((str(subvention), None))
			else:
				ligne_deblocages.append((str(subvention), deblocage[0].montant))
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

	def __str__(self):
		return self.nom

	class Meta:
		ordering = ('nom',)
		unique_together = ('nom', 'mandat',)


	def get_default_index(self):
		"""pour ligne_edit, retourne le rang du choix par défault de"""
		return PosteDepense.objects.filter(
				Q(mandat=self.mandat) | Q(mandat=None)).filter(nom__lt=self.nom).count()