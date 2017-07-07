from django.db import models


class LigneCompta(models.Model):
	"""opérations comptables Elles sont liées à la fois à
	un binet pour que ce soit facile à éditer et à un 
	Mandat pour l'historique"""
	binet = models.ForeignKey('binets.Binet')
	mandat = models.ForeignKey('binets.Mandat')
	date = models.DateField(auto_now_add=False, auto_now=False, 
                                verbose_name="Effectuée le")
	auteur = models.ForeignKey('accounts.Eleve', verbose_name = 'Par')
	description = models.CharField(max_length=200)
	debit = models.FloatField(blank = True, null = True)
	credit = models.FloatField(blank = True, null = True)

	def __str__(self):
		return self.description

	class Meta:
		ordering = ('date',)