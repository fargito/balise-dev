from django.db import models
from binets.models import Eleve, Binet

# modèles pour l'application de comptabilité partagée
# en ligne Balise


################################################
#ces classes sont génériques pour tout le site, elles ont
#vocation à être dans la racine
class TypeBinet(models.Model):
	"""types de binets
	ces types peuvent être
	avec chéquier, sans chéquier, ou compte exté"""
	nom = models.CharField(max_length=30)

	def __str__(self):
		return self.nom


class Binet(models.Model):
	"""table dans la BDD représentant l'ensemble des binets"""
	nom = models.CharField(max_length=100)
	description = models.TextField(null=True) # facultatif
	type_binet = models.ForeignKey('TypeBinet')
	remarques_admins = models.TextField(null=True) # facultatif
	is_active = models.BooleanField()

	def __str__(self):
		return self.nom



class Mandats(models.Model):
	"""correspondance entre le binet et ses membres"""
	binet = models.ForeignKey('Binet')
	#president = models.ForeignKey('Eleve')
	tresorier = models.ForeignKey('Eleve')

	def __str__(self):
		return (self.binet, self.president.promotion)


class Promotion(models.Model):
	"""table des promotions"""
	nom = models.CharField(max_length=4)

	def __str__(self):
		return self.nom


class Eleve(models.Model):
	"""table des eleves"""
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	promotion = models.ForeignKey('Promotion')



##################################################
#ces classes sont spécifiques au module compta

class LigneCompta(models.Model):
	"""opérations comptables"""
	date = models.DateField(auto_now_add=False, auto_now=False, 

                                verbose_name="Dépense effectuée")
	binet = models.ForeignKey('Binet')
	auteur = models.ForeignKey('Eleve')
	description = models.CharField(max_length=200)
	debit = models.FloatField()
	credit = models.FloatField()