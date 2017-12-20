from django.db import models
from django.contrib.auth.models import User
from binets.models import Mandat



class Task(models.Model):
	"""représente une tâche ouverte sur un mandat avec ses différentes variables d'état"""
	mandat = models.ForeignKey(Mandat)
	initiator = models.ForeignKey(User, verbose_name='créée par', related_name='initiator')
	taker = models.ForeignKey(User, verbose_name='attribuée à', related_name='taker')
	finisher = models.ForeignKey(User, verbose_name='fermée par', related_name='finisher')
	creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="créée le")
	take_date = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="attribuée le")
	close_date = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="fermée le")
	is_closed = models.BooleanField(default=False)
	is_urgent = models.BooleanField(default=False)
	due_date = models.DateField(auto_now_add=False, auto_now=False, verbose_name="A faire avant le")
	description = models.TextField()

	class Meta:
		ordering = ('is_urgent', 'due_date',)



class Comment(models.Model):
	"""commentaires sur les tâches ouvertes"""
	task = models.ForeignKey(Task)
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="créée le")
	admin_only = models.BooleanField(default=False) #permet de rendre le commentaire visible uniquement par les kessiers
	text = models.TextField()

	class Meta:
		ordering = ('-creation_date',)
		permissions = (
			('see_all_comments', 'Voir les commentaires admin'),
			)