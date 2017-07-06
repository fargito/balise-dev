from django.db import models
from binets.models import Binet

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
		
	

class VOS(Binet):
	"""ici un VOS. L'attribut promotion correspond à la promotion organisatrice"""
	section = models.ForeignKey('vos.Section')
	#def __init__(self):
	#	self.nom = "VOS {0} {1}".format(self.section, int(self.promotion.nom)+2)
	#	type_binet = "VOS"
	#	Binet.__init__(self)

	def __str__(self):
		return "VOS {0} {1}".format(self.section, int(self.current_promotion.nom)+2)

class Participation(models.Model):
	"""table de participation a un evenement"""
	eleve = models.ForeignKey('accounts.Eleve')
	evenement = models.ForeignKey('vos.VOS')
	participation = models.BooleanField()

	def __str__(self):
		if self.participation:
			return "{0} participe au {1}".format(self.eleve, self.evenement)
		else:
			return "{0} ne participe pas au {1}".format(self.eleve, self.evenement)

class MontantCheque(models.Model):
	"""table des montants des différents chèques"""
	evenement = models.ForeignKey('vos.VOS')
	ordre = models.IntegerField()
	montant = models.DecimalField(max_digits=5, decimal_places=2)	

	def __str__(self):
		return "Chèque n°{0} : {1} €".format(self.ordre, self.montant)

class Encaissement(models.Model):
	"""table des encaissements par élève"""
	evenement = models.ForeignKey('vos.VOS')
	montant = models.ForeignKey('vos.MontantCheque')
	eleve = models.ForeignKey('accounts.Eleve')
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