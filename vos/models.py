from django.db import models

class Evenement(models.Model):
	"""ici un VOS. L'attribut promotion correspond à la promotion organisatrice"""
	section = models.ForeignKey('accounts.Section')
	promotion = models.ForeignKey('accounts.Promotion')	

	def __str__(self):
		return "VOS {1} {2}".format(self.section, self.promotion+2)

class Participation(models.Model):
	"""table de participation a un evenement"""
	eleve = models.ForeignKey('accounts.Eleve')
	evenement = models.ForeignKey('vos.Evenement')
	participation = models.BooleanField()

	def __str__(self):
		if self.participation:
			return "{1} participe au {2}".format(self.eleve, self.evenement)
		else:
			return "{1} ne participe pas au {2}".format(self.eleve, self.evenement)

class MontantCheque(models.Model):
	"""table des montants des différents chèques"""
	evenement = models.ForeignKey('vos.Evenement')
	montant = models.DecimalField(max_digits=5, decimal_places=2)	

	def __str__(self):
		return "{1} €".format(self.montant)

class Encaissement(models.Model):
	"""table des encaissements par élève"""
	evenement = models.ForeignKey('vos.Evenement')
	montant = models.ForeignKey('vos.MontantCheque')
	eleve = models.ForeignKey('accounts.Eleve')
	paye = models.BooleanField()

	def __str__(self):
		return self.montant

class Remboursement(models.Model):
	"""table des remboursements par élève"""
	evenement = models.ForeignKey('vos.Evenement')
	montant = models.DecimalField(max_digits=5, decimal_places=2)
	eleve = models.ForeignKey('accounts.Eleve')
	paye = models.BooleanField()

	def __str__(self):
		return self.montant
