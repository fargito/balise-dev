#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from binets.models import Mandat
from .models import LigneCompta
from subventions.models import VagueSubventions, Subvention, DeblocageSubvention, TypeSubvention
from django.db.models import Q

from .forms import LigneComptaForm, DeblocageSubventionForm, BaseDeblocageSubventionFormSet, CustomDeblocageSubventionFormSet
from binets.forms import DescriptionForm
from django.forms import formset_factory, inlineformset_factory


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
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
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


		# on construit le formset des formulaires pour les déblocages
		DeblocageSubventionFormSet = formset_factory(DeblocageSubventionForm, extra=len(subventions_binet), formset=BaseDeblocageSubventionFormSet)
		# attention contrairement à la modification de déblocages, on doit fournir au formset la liste des subventions
		# pour pouvoir vérifier la compatibilité des déblocages
		deblocage_formset = DeblocageSubventionFormSet(subventions_binet, request.POST or None)


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

	
	debit_subtotal, credit_subtotal = mandat.get_subtotals()
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
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user in authorized['edit'] or request.user.is_staff:
		LigneCompta.objects.get(id=id_ligne).delete()
	return redirect('../')


@login_required
def edit_ligne(request, id_ligne):
	"""permet de modifier une ligne et de rajouter des commentaires dessus"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on récupère toutes les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)

	# on met ensuite dynamiquement les formulaires qui nous intéressent dans un dict
	subventions_names = []
	for subvention in subventions_binet:
		subventions_names.append(
			subvention.vague.type_subvention.nom+' '+subvention.vague.annee)

	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('../')


	ligne = LigneCompta.objects.get(id=id_ligne)
	if request.method == 'POST':
		ligne_form = LigneComptaForm(request.POST, instance=ligne)
		
		# on construit le formset des formulaires pour les déblocages en précisant les instances à modifier
		DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0, formset=CustomDeblocageSubventionFormSet)
		deblocage_edit_formset = DeblocageSubventionFormSet(request.POST, instance=ligne)
		

		# on vérifie la validité du formulaire et on pré-enregistre la ligne
		if ligne_form.is_valid():
			ligne = ligne_form.save(commit=False)
			ligne.modificateur = request.user
			
			# on construit le formset des formulaires pour les déblocages en précisant les instances à modifier
			DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0, formset=CustomDeblocageSubventionFormSet)
			deblocage_edit_formset = DeblocageSubventionFormSet(request.POST, instance=ligne)

			if deblocage_edit_formset.is_valid():
				# on crée les déblocages de subvention qui vont avec la ligne
				for k in range(len(subventions_binet)):
					deblocage = deblocage_edit_formset[k].save()


				ligne.save()

				ligne_form = LigneComptaForm(instance=ligne)
				# on construit le formset des formulaires pour les déblocages en précisant les instances à modifier
				DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0)
				deblocage_edit_formset = DeblocageSubventionFormSet(instance=ligne)

	else:
		ligne_form = LigneComptaForm(instance=ligne)
		# on construit le formset des formulaires pour les déblocages en précisant les instances à modifier
		DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0)
		deblocage_edit_formset = DeblocageSubventionFormSet(instance=ligne)

	return render(request, 'compta/edit_ligne.html', locals())


@login_required
def view_ligne(request, id_ligne):
	"""permet de voir une ligne et de rajouter des commentaires dessus"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on récupère toutes les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)

	# on met ensuite dynamiquement les formulaires qui nous intéressent dans un dict
	subventions_names = []
	for subvention in subventions_binet:
		subventions_names.append(
			subvention.vague.type_subvention.nom+' '+subvention.vague.annee)

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
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	commentaire_form = DescriptionForm(request.POST or None, instance=mandat)

	if commentaire_form.is_valid():
		commentaire_form.save()


	# on récupère toutes les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)

	lignes = LigneCompta.objects.filter(mandat=mandat)
	request.session['active_tab'] = 'Remarques'
	return render(request, 'compta/view_remarques.html', locals())


@login_required
def binet_subventions(request):
	"""vue de la page des subventions du binet"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	# on récupère toutes les subventions du binet
	subventions = Subvention.objects.filter(mandat=mandat)

	request.session['active_tab'] = 'Subventions'
	return render(request, 'compta/binet_subventions.html', locals())



@login_required
def binet_compta_history(request):
	"""affiche la liste des mandats du binet en question auquel a droit d'accéder l'utilisateur"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	request.session['active_tab'] = 'Historique'

	liste_mandats = mandat.binet.get_available_mandats(request.user)

	return render(request, 'compta/binet_compta_history.html', locals())