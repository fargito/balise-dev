#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from binets.models import Mandat
from .forms import LigneComptaForm, DeblocageSubventionForm
from .models import LigneCompta
from subventions.models import VagueSubventions, Subvention, DeblocageSubvention, TypeSubvention
from django.forms import formset_factory
from django.db.models import Q


@login_required
def my_binets(request):
	"""this page allows the user to select the binets
	in which he has a role. If he's admin, he can have them all.
	This views allows the user to place a Binet object in the session.
	It will be implied in the compta module that this Object is in
	th session parameters"""

	if request.user.is_staff:
		liste_mandats = Mandat.objects.all()
	else:
		liste_mandats = Mandat.objects.filter(
			Q(president=request.user) | 
			Q(tresorier=request.user))
	return render(request, 'compta/my_binets.html', locals())


@login_required
def mandat_set(request, id_mandat):
	"""this function's only purpose is to set
	the session variable to id and then redirect to
	mandat_journal"""
	request.session['id_mandat'] = id_mandat
	return redirect('.')


@login_required
def mandat_journal(request):
	"""affiche le journal comptable et permet de le modifier"""
	mandat = Mandat.objects.get(
		id = request.session['id_mandat'])
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	# on récupère toutes les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)
	has_subventions = len(subventions_binet) != 0


	if request.user in authorized['edit'] or request.user.is_staff:
		# on ne met le formulaire en place que si l'user a le doit de modif
		request.session['edit'] = True
		ligne_form = LigneComptaForm(request.POST or None)

		# on met ensuite dynamiquement les formulaires qui nous intéressent dans un dict
		subventions_names = []
		for subvention in subventions_binet:
			subventions_names.append(
				subvention.vague.type_subvention.nom+' '+subvention.vague.annee)
		print(request.POST)

		# on construit le formset
		DeblocageSubventionFormSet = formset_factory(DeblocageSubventionForm, extra=len(subventions_binet))
		deblocage_formset = DeblocageSubventionFormSet(request.POST or None)


		if ligne_form.is_valid() and deblocage_formset.is_valid():
			# on crée une nouvelle ligne comptable pour le mandat
			ligne = ligne_form.save(commit=False)
			ligne.auteur = request.user
			ligne.modificateur = request.user
			ligne.mandat = mandat
			ligne.save()
			ligne_form = LigneComptaForm(None)

			# on crée les déblocages de subvention qui vont avec la ligne
			for k in range(len(subventions_binet)):
				deblocage = deblocage_formset[k].save(commit=False)
				deblocage.ligne_compta = ligne
				deblocage.subvention = subventions_binet[k]
				deblocage.save()
			deblocage_formset = DeblocageSubventionFormSet(None)



	# on récupère toutes les lignes du mandat
	lignes = LigneCompta.objects.filter(mandat=mandat)

	
	debit_total, credit_total = mandat.get_totals()
	balance = credit_total-debit_total
	is_positive = (balance >= 0)

		# pour chacun des éléments dans la barre de nav du module 
	# compta, on doit mettre cette variable pour afficher le choix 
	# d'une couleur différente
	request.session['active_tab'] = 'Journal'
	return render(request, 'compta/journal.html', locals())


@login_required
def delete_ligne(request, id_ligne):
	"""supprime une ligne comptable et redirige vers le journal"""
	mandat = Mandat.objects.get(
		id = request.session['id_mandat'])
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user in authorized['edit'] or request.user.is_staff:
		LigneCompta.objects.get(id=id_ligne).delete()
	return redirect('../')


@login_required
def edit_ligne(request, id_ligne):
	"""permet de modifier une ligne et de rajouter des commentaires dessus"""
	mandat = Mandat.objects.get(
		id = request.session['id_mandat'])
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('../')
	ligne = LigneCompta.objects.get(id=id_ligne)
	if request.method == 'POST':
		ligne_form = LigneComptaForm(request.POST, instance=ligne)
		ligne = ligne_form.save(commit=False)
		ligne.modificateur = request.user
		ligne.save()
		ligne_form = LigneComptaForm(instance=ligne)
	ligne_form = LigneComptaForm(instance=ligne)
	return render(request, 'compta/edit_ligne.html', locals())


@login_required
def view_ligne(request, id_ligne):
	"""permet de voir une ligne et de rajouter des commentaires dessus"""
	mandat = Mandat.objects.get(
		id = request.session['id_mandat'])
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')
	ligne = LigneCompta.objects.get(id=id_ligne)
	return render(request, 'compta/view_ligne.html', locals())


@login_required
def view_remarques(request):
	"""permet de voir toutes les remarques sur les lignes compta et le mandat"""
	mandat = Mandat.objects.get(
		id = request.session['id_mandat'])
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')
	request.session['active_tab'] = 'Remarques'
	return render(request, 'compta/view_remarques.html', locals())


@login_required
def binet_subventions(request):
	"""vue de la page des subventions du binet"""
	mandat = Mandat.objects.get(
		id = request.session['id_mandat'])
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	# on récupère toutes les subventions du binet
	subventions = Subvention.objects.filter(mandat=mandat)
	subventions_dict = {}
	for subvention in subventions:
		subventions_dict[subvention.vague.type_subvention.nom+' '+subvention.vague.annee] = subvention.accorde
	print(subventions_dict)


	request.session['active_tab'] = 'Subventions'
	return render(request, 'compta/binet_subventions.html', locals())