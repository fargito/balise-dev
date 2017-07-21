from django.db import models



class TypeSubvention(models.Model):
	"""définit un type de subvention. Kès mai, Kès février, Forum, etc.
	A priori ne concerne que les subventions pour lesquelles on surveille le déblocage
	(pas les subventions corps par exemple"""
	nom = models.CharField(max_length=30)
	deblocable = models.BooleanField()

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
	postes = models.TextField()

	def __str__(self):
		return '{} du binet {}'.format(self.vague, self.mandat)

	class Meta:
		unique_together = ('vague', 'mandat',)
		ordering = ('-vague', 'mandat',)

	def get_deblocages_list(self):
		"""retourne la liste des déblocages effectués sur cette subvention"""
		return DeblocageSubvention.objects.filter(subvention=self).filter(montant__gt=0)

	def get_deblocages_total(self):
		"""retourne le total débloqué sur cette subvention"""
		deblocages = self.get_deblocages_list()
		debloque = 0
		for deblocage in deblocages:
			if deblocage.montant:
				debloque += deblocage.montant
		return debloque

	def get_rest(self):
		"""retourne ce qui reste de non débloqué de la subvention"""
		return self.accorde-self.get_deblocages_total()



class DeblocageSubvention(models.Model):
	"""cette classe sert à avoir des déblocages sur chaque vague. Elles sont en OneToOne avec une ligne de compta
	et non pas intégrées pour pouvoir rajouter des types de subventions"""
	ligne_compta = models.ForeignKey('compta.LigneCompta')
	subvention = models.ForeignKey(Subvention)
	montant = models.DecimalField(null=True, blank=True,max_digits=9, decimal_places=2)

	class Meta:
		ordering = ('subvention',)
		unique_together = ('ligne_compta', 'subvention',)

	def __str__(self):
		return 'deblocage de '+str(self.montant)+' depense '+str(self.ligne_compta)+' sur '+str(self.subvention)