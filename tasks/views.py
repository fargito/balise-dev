from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Task, Comment

from django.db.models import Q


@login_required
def tasks_home(request):
	"""page sur laquelle on voit toutes ses tasks avec les commentaires
	cette page est juste destinée aux utilisateurs normaux. Les kessiers ont une interface d'administration"""
	try:
		my_mandats = request.user.eleve.get_mandats()
	except:
		return redirect('/')


	# l'utilisateur a droit à toutes les tâches des mandats qu'il a
	search_filter = Q(initiator=request.user)
	for mandat in my_mandats:
		search_filter |= Q(mandat=mandat)

	my_tasks = Task.objects.filter(search_filter)

	return render(request, 'tasks/tasks_home.html', locals())