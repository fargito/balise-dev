from django.db import models
from binets.models import Binet, Mandat

class Section(models.Model):
	"""table des sections"""
	nom = models.CharField(max_length=20)

	class Meta:
		ordering = ('-nom',)

	def __str__(self):
		return self.nom

class EleveVos(models.Model):
	"""eleves par section et promotion"""
	section = models.ForeignKey('vos.Section')
	promotion = models.ForeignKey('accounts.Promotion')
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)


class VOS(models.Model):
	"""ici un VOS. L'attribut promotion correspond à la promotion organisatrice"""
	section = models.ForeignKey('vos.Section')
	#def __init__(self):
	#	self.nom = "VOS {0} {1}".format(self.section, int(self.promotion.nom)+2)
	#	type_binet = "VOS"
	#	Binet.__init__(self)

	def __str__(self):
		return "VOS {0}".format(self.section)


class Participation(models.Model):
	"""table de participation a un evenement"""
	eleve = models.ForeignKey('vos.eleveVos')
	evenement = models.ForeignKey('vos.VOS')
	promotion = models.ForeignKey('accounts.Promotion')
	participation = models.BooleanField()

	def __str__(self):
		if self.participation:
			return "{0} participe au {1}".format(self.eleve, self.evenement)
		else:
			return "{0} ne participe pas au {1}".format(self.eleve, self.evenement)


class MontantCheque(models.Model):
	"""table des montants des différents chèques"""
	evenement = models.ForeignKey('vos.VOS')
	promotion = models.ForeignKey('accounts.Promotion')
	ordre = models.IntegerField()
	montant = models.DecimalField(max_digits=5, decimal_places=2)	

	def __str__(self):
		return "Chèque n°{0} : {1} €".format(self.ordre, self.montant)


class Encaissement(models.Model):
	"""table des encaissements par élève"""
	evenement = models.ForeignKey('vos.VOS')
	montant = models.ForeignKey('vos.MontantCheque')
	eleve = models.ForeignKey('accounts.Eleve')
	promotion = models.ForeignKey('accounts.Promotion')
	paye = models.BooleanField()

	def __str__(self):
		return self.montant


class Remboursement(models.Model):
	"""table des remboursements par élève"""
	evenement = models.ForeignKey('vos.VOS')
	montant = models.DecimalField(max_digits=5, decimal_places=2)
	eleve = models.ForeignKey('accounts.Eleve')
	paye = models.BooleanField()

	def __str__(self):
		return self.montant