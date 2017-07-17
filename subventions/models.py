from django.db import models



class TypeSubvention(models.Model):
	"""définit un type de subvention. Kès mai, Kès février, Forum, etc.
	A priori ne concerne que les subventions pour lesquelles on surveille le déblocage
	(pas les subventions corps par exemple"""
	nom = models.CharField(max_length=30)

	class Meta:
		unique_together = ('nom',)

	def __str__(self):
		return self.nom



class VagueSubventions(models.Model):
	"""définit une table des vagues de subventions"""
	type_subvention = models.ForeignKey(TypeSubvention)
	annee = models.CharField(max_length=4)

	def __str__(self):
		return 'subventions {} {}'.format(self.type_subvention,
		 self.annee)

	class Meta:
		unique_together = ('type_subvention', 'annee')
		ordering = ('-annee',)

	def get_totals(self):
		"""retourne la somme totale demandée et la somme totale accordée"""
		subventions = Subvention.objects.filter(vague=self)
		total_demande, total_accorde = 0,0
		for subvention in subventions:
			total_demande += subvention.demande
			total_accorde += subvention.accorde
		return total_demande, total_accorde
		


	@models.permalink
	def view_self_url(self):
		"""retourne l'url permettant de visualiser la vague
		de subventions"""
		return ('view_vague', [self.id])



class Subvention(models.Model):
	"""définit la table des subventions effectivement accordées"""
	vague = models.ForeignKey(VagueSubventions)
	mandat = models.ForeignKey('binets.Mandat')
	demande = models.DecimalField(null=True, blank=True,max_digits=9, decimal_places=2)
	accorde = models.DecimalField(null=True, blank=True,max_digits=9, decimal_places=2)
	debloque = models.DecimalField(null=True, blank=True,max_digits=9, decimal_places=2)	
	postes = models.TextField()

	def __str__(self):
		return '{} du binet {}'.format(self.vague, self.mandat)

	class Meta:
		unique_together = ('vague', 'mandat',)
		ordering = ('vague', 'mandat',)