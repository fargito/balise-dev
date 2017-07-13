from django.db import models
from django.contrib.auth.models import User

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