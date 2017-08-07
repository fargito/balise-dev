from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Binet, Mandat
from .forms import BinetEditForm, MandatEditForm, BinetCreateForm
from django.db.models import Q

import datetime

from subventions.helpers import generate_ordering_arguments, generate_ordering_links


@login_required
def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	actifs avec les responsables. On dispose des filtres définis dans attributes"""

	# on récupère le paramètre de recherche
	search_arguments = request.GET.get('q', None)

	# on récupère le paramètre d'ordonnance depuis l'url
	ordering = request.GET.get('o', None)
	attributes = ['binet__nom', 'promotion', 'type_binet']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes, only_one=True)

	# on récupères les binets correspondants à la recherche
	if search_arguments:
		# on transfome la chaine brute en liste pour traiter séparément les mots
		search_arguments_list = search_arguments.split()
		# on construit une liste d'argments Q
		search_list = [Q(binet__nom__icontains=q) for q in search_arguments_list]
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
	if search_arguments:
		links_base = 'q=' + search_arguments + '&o='
	else:
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
	try:
		binet = Binet.objects.get(id=id_binet)
	except KeyError:
		return redirect('../')

	next = request.GET.get('next', binet.get_history_url())

	binet_edit_form = BinetEditForm(request.POST or None, instance=binet)

	if binet_edit_form.is_valid():
		if request.POST['validation'] == 'Valider':
			binet_edit_form.save()
		return redirect(next)

	return render(request, 'binets/edit_binet.html', locals())


@staff_member_required
def edit_mandat(request, id_binet, id_mandat):
	try:
		mandat = Mandat.objects.get(
			id = id_mandat)
		binet = Binet.objects.get(id=id_binet)
	except KeyError:
		return redirect('../')

	next = request.GET.get('next', binet.get_history_url())

	# le False correspond à create=False dans le formulaire, ce qui permet d'éditer des mandats existants
	mandat_edit_form = MandatEditForm(binet, False, request.POST or None, instance=mandat)

	if mandat_edit_form.is_valid():
		if request.POST['validation'] == 'Valider':
			mandat_edit_form.save()
		return redirect(next)

	return render(request, 'binets/edit_mandat.html', locals())


@staff_member_required
def new_mandat(request, id_binet):
	try:
		binet = Binet.objects.get(id=id_binet)
	except KeyError:
		return redirect('../')

	next = request.GET.get('next', binet.get_history_url())

	mandat_edit_form = MandatEditForm(binet, True, request.POST or None, initial={'type_binet': binet.get_latest_mandat().type_binet})

	if mandat_edit_form.is_valid():
		if request.POST['validation'] == 'Valider':
			previous_mandat = binet.get_latest_mandat()
			created_mandat = mandat_edit_form.save(commit=False)
			created_mandat.binet = binet
			created_mandat.creator = request.user
			created_mandat.save()
			if previous_mandat:
				previous_mandat.is_displayed = False
				previous_mandat.save()
		return redirect(next)

	return render(request, 'binets/new_mandat.html', locals())


@staff_member_required
def new_binet(request):
	binet_create_form = BinetCreateForm(request.POST or None)

	if binet_create_form.is_valid():
		if request.POST['validation'] == 'Valider':
			# binet = binet_create_form.save()
			# return redirect(binet.get_history_url())
			pass

		return redirect('liste_binets')

	return render(request, 'binets/new_binet.html', locals())



@staff_member_required
def mandat_view_unview(request, id_mandat):
	try:
		mandat = Mandat.objects.get(
			id = id_mandat)
	except KeyError:
		return redirect('../')

	previous = request.GET.get('previous', mandat.binet.get_history_url())

	mandat.is_displayed = not mandat.is_displayed
	mandat.save()

	return redirect(previous)


@staff_member_required
def mandat_activate_deactivate(request, id_mandat):
	try:
		mandat = Mandat.objects.get(
			id = id_mandat)
	except KeyError:
		return redirect('../')

	previous = request.GET.get('previous', mandat.binet.get_history_url())

	if mandat.is_active:
		mandat.passed_date = datetime.datetime.now()

	mandat.is_active = not mandat.is_active
	mandat.save()

	return redirect(previous)