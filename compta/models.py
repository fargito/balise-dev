from django.db import models


class LigneCompta(models.Model):
	"""opérations comptables"""
	binet = models.ForeignKey('binets.Binet')
	date = models.DateField(auto_now_add=False, auto_now=False, 

                                verbose_name="Effectuée le")
	auteur = models.ForeignKey('accounts.Eleve', verbose_name = 'Par')
	description = models.CharField(max_length=200)
	debit = models.FloatField(blank = True, null = True)
	credit = models.FloatField(blank = True, null = True)

	def __str__(self):
		return self.description