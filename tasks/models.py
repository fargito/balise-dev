from django.db import models
from django.contrib.auth.models import User
from binets.models import Mandat



class Task(models.Model):
	"""représente une tâche ouverte sur un mandat avec ses différentes variables d'état"""
	mandat = models.ForeignKey(Mandat)
	initiator = models.ForeignKey(User, verbose_name='créée par', related_name='initiator')
	taker = models.ForeignKey(User, verbose_name='attribuée à', related_name='taker', blank=True, null=True)
	finisher = models.ForeignKey(User, verbose_name='fermée par', related_name='finisher', blank=True, null=True)
	creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="créée le")
	take_date = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="attribuée le", blank=True, null=True)
	close_date = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="fermée le", blank=True, null=True)
	is_closed = models.BooleanField(default=False)
	is_urgent = models.BooleanField(default=False)
	due_date = models.DateField(auto_now_add=False, auto_now=False, verbose_name="A faire avant le")
	title = models.CharField(max_length=20)
	description = models.TextField()

	class Meta:
		ordering = ('is_closed', '-is_urgent', 'due_date',)

	def __str__(self):
		return str(self.initiator) + '@' + str(self.mandat) + ' : ' + self.title



class Comment(models.Model):
	"""commentaires sur les tâches ouvertes"""
	task = models.ForeignKey(Task)
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Envoyé")
	admin_only = models.BooleanField(default=False) #permet de rendre le commentaire visible uniquement par les kessiers
	text = models.TextField()

	class Meta:
		ordering = ('-creation_date',)
		permissions = (
			('see_all_comments', 'Voir les commentaires admin'),
			)

	def __str__(self):
		return str(self.author) + ' - answer@' + str(self.task)[0:20] + ' : ' + self.text[0:20] + '...'