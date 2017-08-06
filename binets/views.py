from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Binet, Mandat
from .forms import SearchForm, BinetEditForm, MandatEditForm
from django.db.models import Q

from subventions.helpers import generate_ordering_arguments, generate_ordering_links


@login_required
def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	actifs avec les responsables. On dispose des filtres définis dans attributes"""

	search_arguments = None
	search_form = SearchForm(request.POST or None)
	if search_form.is_valid():
		search_arguments = search_form.cleaned_data['search']


	# on récupère le paramètre d'ordonnance depuis l'url
	ordering = request.GET.get('o', None)
	attributes = ['binet__nom', 'promotion', 'type_binet']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes, only_one=True)

	# on récupères les binets correspondants à la recherche
	if search_arguments:
		# on transfome la chaine brute en liste pour traiter séparément les mots
		search_arguments = search_arguments.split()
		# on construit une liste d'argments Q
		search_list = [Q(nom__icontains=q) for q in search_arguments]
		# on concatène ces arguments
		search = search_list.pop()
		for item in search_list:
			search |= item


		if arguments:
			liste_mandats = Mandat.objects.filter(search, is_displayed=True).order_by(*arguments)
		else:
			liste_mandats = Mandat.objects.filter(search, is_displayed=True)
	else:
		if arguments:
			liste_mandats = Mandat.objects.filter(is_displayed=True).order_by(*arguments)
		else:
			liste_mandats = Mandat.objects.filter(is_displayed=True)
	# on ordonne les résultats
	if arguments:
		liste_mandats = liste_mandats.order_by(*arguments)


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


@staff_member_required
def edit_binet(request, id_binet):
	binet = Binet.objects.get(id=id_binet)

	binet_edit_form = BinetEditForm(request.POST or None, instance=binet)
	if binet_edit_form.is_valid():
		binet_edit_form.save()

	return render(request, 'binets/edit_binet.html', locals())