from django.db import models
from django.contrib.auth.models import User


class ProblemDepart(models.Model):
	"""permet d'ajouter des problèmes pour un élève sur son circuit de départ"""
	user = models.ForeignKey(User)
	description = models.CharField(max_length=300)
	resolved = models.BooleanField(default=False)

	@models.permalink
	def mark_as_resolved_url(self):
		return ('mark_problem_as_resolved', [self.id])

	def __str__(self):
		return str(self.user) + ': ' + str(self.description)