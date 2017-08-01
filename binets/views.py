from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Binet, Mandat

from subventions.helpers import generate_ordering_arguments, generate_ordering_links


@login_required
def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	actifs avec les responsables. On dispose des filtres définis dans attributes"""

	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	
	attributes = ['nom', 'mandat__promotion']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes)

	# on récupère les arguments filtrés
	if arguments:
		liste_binets = Binet.objects.all().order_by(*arguments)
	else:
		liste_binets = Binet.objects.all()

	# on génère les liens qui serviront à l'ordonnance dans la page
	# si aucun n'a été activé, par défault c'est par nom de binet (index 0)
	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	links_base = '?o='
	ordering_links = list(reversed(generate_ordering_links(ordering, attributes, links_base)))


	return render(request, 'binets/all_binets.html', locals())


@login_required
def binet_history(request, id_binet):
	"""generates the view for the binet history"""
	binet = Binet.objects.get(
		id=id_binet)
	liste_mandats = Mandat.objects.filter(
		binet=binet)
	return render(request, 'binets/binet_history.html', locals())