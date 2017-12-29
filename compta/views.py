#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse

from binets.models import Mandat, TypeBinet
from .models import LigneCompta, PosteDepense, Evenement
from subventions.models import VagueSubventions, Subvention, DeblocageSubvention, TypeSubvention
from django.db.models import Q

from django import forms
from .forms import LigneComptaForm, DeblocageSubventionForm, BaseDeblocageSubventionFormSet, CustomDeblocageSubventionFormSet
from .forms import PosteDepenseForm, SearchLigneForm, SearchLigneFormPolymedia, EvenementForm, PosteAndCommentForm
from binets.forms import DescriptionForm
from django.forms import formset_factory, inlineformset_factory
from imports.forms import ImportFileForm

from imports.file_handlers import file_handler, create_lignes_compta, validate_import_lignes

from subventions.helpers import generate_ordering_arguments, generate_ordering_links

from datetime import datetime
import pandas


@login_required
def my_binets(request):
	"""this page allows the user to select the binets
	in which he has a role.
	This views allows the user to place a Binet object in the session.
	It will be implied in the compta module that this Object is in
	the session parameters"""

	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	
	attributes = ['binet', 'promotion', 'type_binet', 'is_active']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes)

	
	# on génère les liens qui serviront à l'ordonnance dans la page
	# si aucun n'a été activé, par défault c'est par nom de binet (index 0)
	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	links_base = '?o='
	ordering_links = list(reversed(generate_ordering_links(ordering, attributes, links_base)))


	# on récupère les binets en fonction du statut de l'utilisateur et des choix d'ordre
	if arguments:
		liste_mandats = Mandat.objects.filter(
			Q(president=request.user) | 
			Q(tresorier=request.user)).order_by(*arguments)
	else:
		liste_mandats = Mandat.objects.filter(
			Q(president=request.user) | 
			Q(tresorier=request.user))

	return render(request, 'compta/my_binets.html', locals())


@login_required
def mandat_set(request, id_mandat):
	"""this function's only purpose is to set
	the session variable to id and then redirect to
	mandat_journal, or to the optional 'next' parameter"""
	request.session['id_mandat'] = id_mandat
	# setting the return button to go where we come from
	request.session['previous'] = request.GET.get('previous', '../')
	request.session['passation_redirect'] = request.GET.get('passation_redirect', None)
	# on utilise .get and set default to '.'
	return redirect(request.GET.get('next', '.'))


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
		return redirect(request.session['previous'])

	# on récupère toutes les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)
	has_subventions = len(subventions_binet) != 0


	if request.user in authorized['edit'] or request.user.is_staff:
		# on ne met le formulaire en place que si l'user a le doit de modif
		request.session['edit'] = True

		# comme le champ poste_depense a besoin du mandat pour être instancié, on doit le créer juste avant l'instanciation
		# du formulaire
		LigneComptaForm.base_fields['poste_depense'] = forms.ModelChoiceField(
			queryset=PosteDepense.objects.filter(
				Q(mandat=mandat) | Q(mandat=None)), required=False, empty_label="Aucun")
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
			# comme le champ poste_depense a besoin du mandat pour être instancié, on doit le créer juste avant l'instanciation
			# du formulaire
			LigneComptaForm.base_fields['poste_depense'] = forms.ModelChoiceField(
				queryset=PosteDepense.objects.filter(
					Q(mandat=mandat) | Q(mandat=None)), required=False, empty_label="Aucun")
			ligne_form = LigneComptaForm(None)

			# on crée les déblocages de subvention qui vont avec la ligne
			for k in range(len(subventions_binet)):
				deblocage = deblocage_formset[k].save(commit=False)
				deblocage.ligne_compta = ligne
				deblocage.subvention = subventions_binet[k]
				deblocage.save()
			deblocage_formset = DeblocageSubventionFormSet(None)

	else:
		request.session['edit'] = False


	# ici on récupère les lignes du mandat, en les ordonnant selon les filtres donnés
	# ces filtres sont donnés par ordre dans la liste d'attributs donnée
	# ces attribut n'incluent pas les subventions, qu'on peut isoler dans la partie subventions

	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	attributes = ['facture_ok', 'date', 'reference', 'description', 'poste_depense', 'debit', 'credit']
	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes)
	# on récupère toutes les lignes du mandat
	# on récupère les arguments filtrés
	if arguments:
		lignes = LigneCompta.objects.filter(mandat=mandat).order_by(*arguments)
	else:
		lignes = LigneCompta.objects.filter(mandat=mandat)

	# on génère les liens qui serviront à l'ordonnance dans la page
	# si aucun n'a été activé, par défault c'est par date (index 0)
	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	links_base = '?o='
	ordering_links = list(reversed(generate_ordering_links(ordering, attributes, links_base)))
	
	# paramètre de vision de l'aide
	help_activated = request.GET.get('help', 'false') == 'true'

	has_chequier = not(mandat.type_binet.nom == "Sans chéquier")

	# on récupère les totaux pour le mandat
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
		ligne =	LigneCompta.objects.get(id=id_ligne)
		if not ligne.is_locked or request.user.is_staff:
			# si l'écriture est locked, seuls les admins peuvent la supprimer
			# de même si des déblocages versés ont été fait dessus
			
			if not(ligne.has_versed_deblocage()) or request.user.is_staff:
				ligne.delete()
	return redirect('../')


@login_required
def edit_ligne(request, id_ligne):
	"""permet de modifier une ligne et de rajouter des commentaires dessus"""
	try:
		ligne = LigneCompta.objects.get(id=id_ligne)
		mandat = ligne.mandat
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


	if ligne.is_locked and not request.user.is_staff:
		# si la ligne est locked, seuls les admins peuvent la supprimer
		return redirect('../')

	# nécessaire si l'appel n'est pas effectué depuis le journal
	request.session['id_mandat'] = mandat.id

	if request.method == 'POST':
		# comme le champ poste_depense a besoin du mandat pour être instancié, on doit le créer juste avant l'instanciation
		# du formulaire
		# on calcule le rang du choix par défaut
		if ligne.poste_depense:
			initial_choice_index = ligne.poste_depense.get_default_index()
		else:
			initial_choice_index = 0
		LigneComptaForm.base_fields['poste_depense'] = forms.ModelChoiceField(
			queryset=PosteDepense.objects.filter(
				Q(mandat=mandat) | Q(mandat=None)), required=False, empty_label="Aucun", initial=initial_choice_index)
		ligne_form = LigneComptaForm(request.POST, instance=ligne)
		
		# on construit le formset des formulaires pour les déblocages en précisant les instances à modifier
		DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0, formset=CustomDeblocageSubventionFormSet)
		deblocage_edit_formset = DeblocageSubventionFormSet(request.POST, instance=ligne)



		# on vérifie la validité du formulaire et on pré-enregistre la ligne
		if ligne_form.is_valid():
			ligne = ligne_form.save(commit=False)
			ligne.modificateur = request.user
			
			# on reconstruit le formset des formulaires avec les données modifiées pour les déblocages en précisant les instances à modifier
			DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0, formset=CustomDeblocageSubventionFormSet)
			deblocage_edit_formset = DeblocageSubventionFormSet(request.POST, instance=ligne)

			if deblocage_edit_formset.is_valid():
				# on crée les déblocages de subvention qui vont avec la ligne
				for k in range(len(subventions_binet)):
					deblocage = deblocage_edit_formset[k].save()


				ligne.save()

				return redirect('../')
				

	else:
		# comme le champ poste_depense a besoin du mandat pour être instancié, on doit le créer juste avant l'instanciation
		# du formulaire

		if ligne.poste_depense:
			initial_choice_index = ligne.poste_depense.get_default_index()
		else:
			initial_choice_index = 0

		LigneComptaForm.base_fields['poste_depense'] = forms.ModelChoiceField(
			queryset=PosteDepense.objects.filter(
				Q(mandat=mandat) | Q(mandat=None)), required=False, empty_label="Aucun", initial=initial_choice_index)
		ligne_form = LigneComptaForm(instance=ligne)
		# on construit le formset des formulaires pour les déblocages en précisant les instances à modifier
		DeblocageSubventionFormSet = inlineformset_factory(LigneCompta, DeblocageSubvention, fields=('montant',), extra=0)
		deblocage_edit_formset = DeblocageSubventionFormSet(instance=ligne)

	return render(request, 'compta/edit_ligne.html', locals())


@staff_member_required
def lock_unlock_ligne(request, id_ligne):
	"""permet de verrouiller ou de déverrouiller une ligne Accessible uniquement pour les admins"""
	if not request.user.is_staff:
		return redirect(request.GET.get('next', '../'))
	ligne = LigneCompta.objects.get(id=id_ligne)
	ligne.is_locked =  not (ligne.is_locked)
	ligne.save()
	return redirect(request.GET.get('next', '../'))


@permission_required('compta.validate_polymedia')
def lock_unlock_ligne_polymedia(request, id_ligne):
	"""permet de verrouiller ou de déverrouiller des dépense polymédia
	Accessible à tous les kessiers et Zaza"""
	ligne = LigneCompta.objects.get(id=id_ligne)
	ligne.is_locked =  not (ligne.is_locked)
	ligne.save()
	return redirect(request.GET.get('next', '../'))


@staff_member_required
def lock_unlock_all(request):
	"""permet de verrouiller toutes les opérations d'un binet.
	Accessible uniquement aux admins"""
	if not request.user.is_staff:
		return redirect(request.GET.get('next', '../'))

	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	lignes = LigneCompta.objects.filter(mandat=mandat)
	# si toutes les lignes sont locked, il faut tout unlock
	to_put = not mandat.is_all_locked()
	for ligne in lignes:
		ligne.is_locked = to_put
		ligne.save()

	return redirect(request.GET.get('next', '../'))

@login_required
def check_uncheck_ligne(request, id_ligne):
	"""permet de checker ou unchecker une ligne accessible aux personnes qui ont le droit edit"""
	next = request.GET.get('next', '../')
	try:
		ligne = LigneCompta.objects.get(id=id_ligne)
		mandat = ligne.mandat
	except KeyError:
		return redirect(next)

	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect(next)

	# dans le cas ou l'appel à la vue de la ligne s'est effectuée depuis un autre endroit que le journal il est possible que le mandat en mémoire ne soit pas bon
	request.session['id_mandat'] = mandat.id


	ligne = LigneCompta.objects.get(id=id_ligne)
	ligne.facture_ok =  not (ligne.facture_ok)
	ligne.save()
	return redirect(next)

	

@login_required
def view_ligne(request, id_ligne):
	"""permet de voir une ligne et de rajouter des commentaires dessus. On peut également modifier le poste de dépense"""
	try:
		ligne = LigneCompta.objects.get(id=id_ligne)
		mandat = ligne.mandat
	except KeyError:
		return redirect('../')

	# on récupère la liste des utilisateurs habilités
	# à supprimer la ligne
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	# dans le cas ou l'appel à la vue de la ligne s'est effectuée depuis un autre endroit que le journal il est possible que le mandat en mémoire ne soit pas bon
	request.session['id_mandat'] = mandat.id

	# on récupère toutes les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)

	# on met ensuite dynamiquement les formulaires qui nous intéressent dans un dict
	subventions_names = []
	for subvention in subventions_binet:
		subventions_names.append(
			subvention.vague.type_subvention.nom+' '+subvention.vague.annee)


	poste_form = PosteAndCommentForm(mandat, request.POST, instance=ligne)

	if request.method == 'POST':
		if poste_form.is_valid():
			ligne = poste_form.save(commit=False)
			ligne.modificateur = request.user
			ligne.save()

	
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
		return redirect(request.session['previous'])

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
	# à voir les subventions
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect(request.session['previous'])

	# on récupère toutes les subventions du binet
	subventions = Subvention.objects.filter(mandat=mandat)

	request.session['active_tab'] = 'Subventions'
	return render(request, 'compta/binet_subventions.html', locals())


@login_required
def binet_bilan(request):
	"""vue du bilan du binet par les utilisateurs, avec répartition par poste de dépense"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à voir les subventions
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect(request.session['previous'])

	# on récupère tous les postes de dépense du mandat et les postes génériques
	postes = PosteDepense.objects.filter(Q(mandat=mandat) | Q(mandat=None))

	evenements = Evenement.objects.filter(mandat=mandat)

	# on récupère aussi les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)

	# on met en forme le tableau de résultats partiels par poste
	postes_with_total = []
	previsionnel_balance_total = 0
	previsionnel_debit_total = 0
	previsionnel_credit_total = 0

	evenements_with_totals = []
	evenement_is_even = False # on met un compteur pour savoir s'il est pair ou non pour la couleur du tableau

	# POSTES DEFINIS ET DANS DES EVENEMENTS
	for evenement in evenements:
		evenement_postes = postes.filter(evenement=evenement)
		evenement_postes_with_total = []
		previsionnel_balance_evenement = 0
		previsionnel_debit_evenement = 0
		previsionnel_credit_evenement = 0
		reel_balance_evenement = 0
		reel_debit_evenement = 0
		reel_credit_with_deblocages_evenement = 0
		diff_balance_evenement = 0
		for poste_depense in evenement_postes:
			poste_totals = get_poste_totals(poste_depense, mandat)
			previsionnel_balance_total += poste_totals['previsionnel_subtotal']
			previsionnel_debit_total += poste_totals['previsionnel_debit']
			previsionnel_credit_total += poste_totals['previsionnel_credit']
			previsionnel_balance_evenement += poste_totals['previsionnel_subtotal']
			previsionnel_debit_evenement += poste_totals['previsionnel_debit']
			previsionnel_credit_evenement += poste_totals['previsionnel_credit']
			reel_balance_evenement += poste_totals['reel_subtotal']
			reel_debit_evenement += poste_totals['reel_debit']
			reel_credit_with_deblocages_evenement += poste_totals['reel_credit_with_deblocages']
			diff_balance_evenement += poste_totals['diff_subtotal']
			# gestion avec les événements
			evenement_postes_with_total.append(poste_totals)

			# gestion avec les postes seuls
			postes_with_total.append(poste_totals)

		if evenement_is_even: color = 'compta-even'
		else: color = 'compta-odd'

		evenements_with_totals.append({
			"evenement": evenement,
			"totals": evenement_postes_with_total,
			"nb_postes": len(evenement_postes_with_total) + 1,
			"is_even": evenement_is_even,
			"color": color,
			"is_not_empty": len(evenement_postes) > 0,
			"previsionnel_balance_evenement": previsionnel_balance_evenement,
			"previsionnel_debit_evenement": previsionnel_debit_evenement,
			"previsionnel_credit_evenement": previsionnel_credit_evenement,
			"reel_balance_evenement": reel_balance_evenement,
			"reel_debit_evenement": reel_debit_evenement,
			"reel_credit_with_deblocages_evenement": reel_credit_with_deblocages_evenement,
			"diff_balance_evenement": diff_balance_evenement,
			"reel_balance_evenement_is_positive": reel_balance_evenement >= 0,
			"previsionnel_balance_evenement_is_positive": previsionnel_balance_evenement >= 0,
			"diff_balance_evenement_is_positive": diff_balance_evenement >= 0,
			})
		evenement_is_even = not evenement_is_even


	# POSTES DEFINIS SANS EVENEMENT
	postes_alone = postes.filter(evenement=None)

	no_event_postes_totals = []
	no_event_previsionnel_balance = 0
	no_event_previsionnel_credit = 0
	no_event_previsionnel_debit = 0
	no_event_reel_balance = 0
	no_event_reel_debit = 0
	no_event_reel_credit_with_deblocages = 0
	no_event_diff_balance = 0
	for poste_depense in postes_alone:
		poste_totals = get_poste_totals(poste_depense, mandat)
		previsionnel_balance_total += poste_totals['previsionnel_subtotal']
		previsionnel_debit_total += poste_totals['previsionnel_debit']
		previsionnel_credit_total += poste_totals['previsionnel_credit']
		no_event_previsionnel_balance += poste_totals['previsionnel_subtotal']
		no_event_reel_balance += poste_totals['reel_subtotal']
		no_event_previsionnel_debit += poste_totals['previsionnel_debit']
		no_event_previsionnel_credit += poste_totals['previsionnel_credit']
		no_event_reel_debit += poste_totals['reel_debit']
		no_event_reel_credit_with_deblocages += poste_totals['reel_credit_with_deblocages']
		no_event_diff_balance += poste_totals['diff_subtotal']
		postes_with_total.append(poste_totals)
		no_event_postes_totals.append(poste_totals)


	# LIGNES SANS POSTE SPECIFIE
	# on récupère ensuite les lignes non spécifiées
	poste_totals = get_poste_totals(None, mandat)
	previsionnel_balance_total += poste_totals['previsionnel_subtotal']
	previsionnel_debit_total += poste_totals['previsionnel_debit']
	previsionnel_credit_total += poste_totals['previsionnel_credit']
	no_event_previsionnel_balance += poste_totals['previsionnel_subtotal']
	no_event_reel_balance += poste_totals['reel_subtotal']
	no_event_diff_balance += poste_totals['diff_subtotal']
	no_event_previsionnel_debit += poste_totals['previsionnel_debit']
	no_event_previsionnel_credit += poste_totals['previsionnel_credit']
	no_event_reel_debit += poste_totals['reel_debit']
	no_event_reel_credit_with_deblocages += poste_totals['reel_credit_with_deblocages']
	postes_with_total.append(poste_totals)
	no_event_postes_totals.append(poste_totals)

	if evenement_is_even: color = 'compta-even'
	else: color = 'compta-odd'

	# on est obligés de compter pour savoir combien de span va devoir faire la dernière ligne
	compteur = 0
	for poste in no_event_postes_totals:
		has_mandat = False

		try:
			if poste['poste_depense'].mandat:
				has_mandat = True
		except AttributeError:
			pass

		if has_mandat or poste['is_not_empty']:
			compteur += 1

	evenements_with_totals.append({
		"evenement": "Non spécifié",
		"totals": no_event_postes_totals,
		"nb_postes": compteur + 1,
		"is_even": evenement_is_even,
		"color": color,
		"is_not_empty": True,
		"previsionnel_balance_evenement": no_event_previsionnel_balance,
		"previsionnel_debit_evenement": no_event_previsionnel_debit,
		"previsionnel_credit_evenement": no_event_previsionnel_credit,
		"reel_balance_evenement": no_event_reel_balance,
		"reel_debit_evenement": no_event_reel_debit,
		"reel_credit_with_deblocages_evenement": no_event_reel_credit_with_deblocages,
		"diff_balance_evenement": no_event_diff_balance,
		"reel_balance_evenement_is_positive": no_event_reel_balance >= 0,
		"previsionnel_balance_evenement_is_positive": no_event_previsionnel_balance >= 0,
		"diff_balance_evenement_is_positive": no_event_diff_balance >= 0,
		})


	# on s'occupe ensuite du bilan global qui est affiché en haut de la page
	reel_debit_total, reel_credit_with_deblocages_total = mandat.get_totals()
	reel_balance_total = mandat.get_balance()
	diff_balance_total = - previsionnel_balance_total + reel_balance_total

	reel_balance_total_is_positive = reel_balance_total >= 0
	previsionnel_balance_total_is_positive = previsionnel_balance_total >= 0
	diff_balance_total_is_positive = diff_balance_total >= 0

	request.session['active_tab'] = 'Bilan'
	return render(request, 'compta/binet_bilan.html', locals())


def get_poste_totals(poste_depense, mandat):
	"""fonction d'aide, retourne les totaux pour le bilan pour un poste de dépense donné.
	Si le poste est None, fonctionnement un peu différent"""
	# on récupère d'abord toutes les lignes associées avec des postes de dépense du mandat
	if poste_depense:
		lignes = LigneCompta.objects.filter(poste_depense=poste_depense, mandat=mandat)
		previsionnel_debit = poste_depense.previsionnel_debit
		previsionnel_credit = poste_depense.previsionnel_credit
		previsionnel_subtotal = previsionnel_credit - previsionnel_debit

	else:
		lignes = LigneCompta.objects.filter(poste_depense=None, mandat=mandat)
		previsionnel_debit = 0
		previsionnel_credit = 0
		previsionnel_subtotal = 0

	# on récupère aussi les subventions du binet
	subventions_binet = Subvention.objects.filter(mandat=mandat)


	subtotal_debit_poste = 0
	subtotal_credit_poste = 0
	subtotals_deblocages_poste = [[subvention, 0] for subvention in subventions_binet]

	for ligne in lignes:
		if ligne.debit:
			subtotal_debit_poste += ligne.debit
			# si la ligne est un débit on incrémente les compteurs des déblocages pour les différentes subventions
			k = 0
			for subvention in subventions_binet:
				montant_deblocage = DeblocageSubvention.objects.get(ligne_compta=ligne, subvention=subvention).montant
				if montant_deblocage:
					subtotals_deblocages_poste[k][1] += montant_deblocage

				k += 1
		if ligne.credit:
			subtotal_credit_poste += ligne.credit

	# on fait la sous_somme du poste
	subtotal_deblocages = 0
	for deblocage in subtotals_deblocages_poste:
		subtotal_deblocages += deblocage[1]
	subtotal_poste = subtotal_credit_poste + subtotal_deblocages - subtotal_debit_poste


	if not poste_depense:
		poste_depense = "Non spécifié"

	return {
		'poste_depense': poste_depense,
		'previsionnel_debit': previsionnel_debit,
		'previsionnel_credit': previsionnel_credit,
		'previsionnel_subtotal': previsionnel_subtotal,
		'previsionnel_is_positive': previsionnel_subtotal >= 0,
		'reel_debit': subtotal_debit_poste,
		'reel_credit': subtotal_credit_poste,
		'reel_credit_with_deblocages': subtotal_deblocages + subtotal_credit_poste,
		'reel_deblocages': subtotals_deblocages_poste,
		'reel_subtotal': subtotal_poste,
		'reel_is_positive': subtotal_poste >= 0,
		'diff_debit': - subtotal_debit_poste + previsionnel_debit,
		'diff_debit_is_positive': - subtotal_debit_poste + previsionnel_debit >= 0,
		'diff_credit': subtotal_credit_poste + subtotal_deblocages - previsionnel_credit,
		'diff_credit_is_positive': subtotal_credit_poste + subtotal_deblocages - previsionnel_credit >= 0,
		'diff_subtotal': subtotal_poste - previsionnel_subtotal,
		'diff_subtotal_is_positive': subtotal_poste - previsionnel_subtotal >= 0,
		'is_not_empty': len(lignes) > 0,
		'nb_recettes': len(subtotals_deblocages_poste) + 1,
		}


@login_required
def binet_compta_history(request):
	"""affiche la liste des mandats du binet en question auquel a droit d'accéder l'utilisateur"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on récupère la liste des utilisateurs habilités
	# à voir l'historique
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect(request.session['previous'])


	liste_mandats = mandat.binet.get_available_mandats(request.user)

	request.session['active_tab'] = 'Historique'
	return render(request, 'compta/binet_compta_history.html', locals())


@login_required
def import_lignes(request):
	"""this view allows the user to import compta operations"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à importer des opérations
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	if request.method == 'POST':
		if request.POST['validation'] == 'Upload':
			import_form = ImportFileForm(request.POST, request.FILES)

			if import_form.is_valid():
				# on copie l'import en mémoire
				date = datetime.today()
				pathname = 'imports/logs/lignes_imports/import_compta_'+\
					str(mandat)+'_'+str(date.year)+'_'+\
					str(date.month)+'_'+str(date.day)+' '+str(
					date.hour)+'_'+str(date.minute)
				
				request.session['pathname'] = pathname
				# on enregistre le fichier temporaire
				file_handler(request.FILES['excel_file'], pathname)

				# on redirige vers la validation
				sent = False
				# on lit les données importées et on les met dans un dict
				imported_lignes = pandas.read_excel(open(pathname, 'rb'), sheetname=0, na_values = ['-'])
				imported_lignes = imported_lignes.transpose().to_dict().values()


				# on vérifie que l'import est correct
				is_valid, parsed_import_list = validate_import_lignes(request, imported_lignes, mandat)

				request.session['messages'] = []
				request.session['messages'].append('Copied the file in the database')

				return render(request, 'compta/import_lignes_confirm.html', locals())
		else:
			if request.POST['validation'] == 'Valider':
				imported_lignes = pandas.read_excel(open(request.session[
					'pathname'], 'rb'), sheetname=0, na_values = ['-'])
				imported_lignes = imported_lignes.transpose().to_dict().values()
				# on vérifie que l'import est correct et on obtient la liste nettoyée
				is_valid, parsed_import_list = validate_import_lignes(request, imported_lignes, mandat)

				create_lignes_compta(request, parsed_import_list, mandat)
				# on supprime le fichier temporaire
				del request.session['pathname']
				sent = True


			if request.POST['validation'] == 'Annuler':
				# on supprime le fichier temporaire
				del request.session['pathname']
				request.session['messages'] = ['Requête annulée']
				sent = True

			return redirect('/compta/journal')

	else:
		import_form = ImportFileForm()

	request.session['active_tab'] = 'Importer des opérations'
	return render(request, 'compta/import_lignes.html', locals())


@login_required
def create_poste_depense(request):
	"""permet de créer un poste de dépense pour le mandat"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à créer des postes
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	poste_depense_form = PosteDepenseForm(mandat, None, request.POST or None)

	if request.method == 'POST':
		if poste_depense_form.is_valid():
			created_poste_depense = poste_depense_form.save(commit=False)
			created_poste_depense.mandat = mandat
			created_poste_depense.save()

			return redirect(request.GET.get('next', '../'))

	return render(request, 'compta/create_poste_depense.html', locals())


@login_required
def edit_poste_depense(request, id_poste):
	"""permet de créer un poste de dépense pour le mandat"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à créer des postes
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	try:
		poste = PosteDepense.objects.get(id=id_poste)
	except KeyError:
		return redirect('../')

	# on vérifie aussi que le poste qu'on cherche à éditer appartient bien au mandat voulu
	if mandat != poste.mandat:
		return redirect('/compta/journal')

	poste_depense_form = PosteDepenseForm(mandat, poste.nom, request.POST or None, instance=poste)

	if request.method == 'POST':
		if poste_depense_form.is_valid():
			poste_depense_form.save()

			return redirect(request.GET.get('next', '../'))

	return render(request, 'compta/create_poste_depense.html', locals())


@login_required
def delete_poste_depense(request, id_poste):
	"""permet de détruire un poste de dépense si et seulement si il est vide"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à supprimer des postes
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	# on récupère la redirection
	next = request.GET.get('next', '../')

	try:
		poste = PosteDepense.objects.get(id=id_poste)
	except:
		return redirect(next)

	if LigneCompta.objects.filter(poste_depense=poste).count() == 0:
		poste.delete()

	return redirect(next)

@login_required
def create_evenement(request):
	"""permet de créer un événement pour le mandat"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à créer des postes
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	evenement_form = EvenementForm(mandat, None, None, request.POST or None)

	if request.method == 'POST':
		if evenement_form.is_valid():
			created_evenement = evenement_form.save(commit=False)
			created_evenement.mandat = mandat
			created_evenement.save()

			return redirect(request.GET.get('next', '../'))

	return render(request, 'compta/create_evenement.html', locals())


@login_required
def edit_evenement(request, id_evenement):
	"""permet de modifier un événement"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à créer des postes
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	try:
		evenement = Evenement.objects.get(id=id_evenement)
	except KeyError:
		return redirect('../')

	# on vérifie aussi que le poste qu'on cherche à éditer appartient bien au mandat voulu
	if mandat != evenement.mandat:
		return redirect('/compta/journal')

	evenement_form = EvenementForm(mandat, evenement.nom, evenement.code, request.POST or None, instance=evenement)

	if request.method == 'POST':
		if evenement_form.is_valid():
			evenement_form.save()

			return redirect(request.GET.get('next', '../'))

	return render(request, 'compta/create_evenement.html', locals())


@login_required
def delete_evenement(request, id_evenement):
	"""permet de détruire un événement si et seulement si il est vide"""
	try:
		mandat = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')

	# on vérifie qui est autorisé à supprimer des postes
	authorized = mandat.get_authorized_users()
	if request.user not in authorized['edit'] and not(request.user.is_staff):
		return redirect('/compta/journal')

	# on récupère la redirection
	next = request.GET.get('next', '../')

	try:
		evenement = Evenement.objects.get(id=id_evenement)
	except:
		return redirect(next)

	if PosteDepense.objects.filter(evenement=evenement).count() == 0:
		evenement.delete()

	return redirect(next)


@staff_member_required
def seance_cheques(request):
	"""permet d'effectuer une séance de chèques pour les binets sans chéquiers"""
	max_requests = float(request.GET.get('max_requests', 50))

	type_binet_default = TypeBinet.objects.get(nom='Sans chéquier')
	type_binet_optional = TypeBinet.objects.get(nom='Avec chéquier')
	

	search_ligne_form = SearchLigneForm(request.POST or None)
	if search_ligne_form.is_valid() and request.POST['validation'] == 'Rechercher':
		# on construit au fur et à mesure le filtre qu'on va appliquer à la base de données en restreignant toujours
		# le nombre de requêtes à max_requests
		cleaned_data = search_ligne_form.cleaned_data
		if cleaned_data['include_others']:
			filter_arg = Q(mandat__type_binet=type_binet_default) | Q(mandat__type_binet=type_binet_optional)
		else:
			filter_arg = Q(mandat__type_binet=type_binet_default)

		if not cleaned_data['include_locked']:
			filter_arg &= Q(is_locked=False)

		if cleaned_data['promotion']:
			filter_arg &= Q(mandat__promotion=cleaned_data['promotion'])

		if cleaned_data['binet']:
			filter_arg &= Q(mandat__binet__nom__icontains=cleaned_data['binet'])

		if cleaned_data['poste']:
			filter_arg &= Q(poste_depense__nom__icontains=cleaned_data['poste'])

		if cleaned_data['reference']:
			filter_arg &= Q(reference=cleaned_data['reference'])

		if cleaned_data['date_debut']:
			filter_arg &= Q(date__gte=cleaned_data['date_debut'])

		if cleaned_data['date_fin']:
			filter_arg &= Q(date__lte=cleaned_data['date_fin'])

		if cleaned_data['montant_bas']:
			filter_arg &= (Q(debit__gte=cleaned_data['montant_bas']) | Q(credit__gte=cleaned_data['montant_bas']))

		if cleaned_data['montant_haut']:
			filter_arg &= (Q(debit__lte=cleaned_data['montant_haut']) | Q(credit__lte=cleaned_data['montant_haut']))

		lignes = LigneCompta.objects.filter(filter_arg)#[0:max_requests]

	else:
		lignes = LigneCompta.objects.filter(mandat__type_binet=type_binet_default, is_locked=False)[0:max_requests]

	return render(request, 'compta/seance_cheques.html', locals())


@permission_required('compta.validate_polymedia')
def validate_polymedia(request):
	"""permet de valider les devis polymédia et magnan des binets"""

	search_ligne_form = SearchLigneFormPolymedia(request.POST or None)
	if search_ligne_form.is_valid() and request.POST['validation'] == 'Rechercher':
		# on construit au fur et à mesure le filtre qu'on va appliquer à la base de données en restreignant toujours
		# le nombre de requêtes à max_requests
		cleaned_data = search_ligne_form.cleaned_data
		filter_arg = Q(Q(poste_depense__nom="Polymédia") | Q(poste_depense__nom="Magnan"))

		if not cleaned_data['include_locked']:
			filter_arg &= Q(is_locked=False)

		if cleaned_data['promotion']:
			filter_arg &= Q(mandat__promotion=cleaned_data['promotion'])

		if cleaned_data['binet']:
			filter_arg &= Q(mandat__binet__nom__icontains=cleaned_data['binet'])

		if cleaned_data['date_debut']:
			filter_arg &= Q(date__gte=cleaned_data['date_debut'])

		if cleaned_data['date_fin']:
			filter_arg &= Q(date__lte=cleaned_data['date_fin'])

		if cleaned_data['montant_bas']:
			filter_arg &= (Q(debit__gte=cleaned_data['montant_bas']) | Q(credit__gte=cleaned_data['montant_bas']))

		if cleaned_data['montant_haut']:
			filter_arg &= (Q(debit__lte=cleaned_data['montant_haut']) | Q(credit__lte=cleaned_data['montant_haut']))

		lignes = LigneCompta.objects.filter(filter_arg)

	else:
		lignes = LigneCompta.objects.filter(Q(Q(poste_depense__nom="Polymédia") | Q(poste_depense__nom="Magnan")), is_locked=False)

	return render(request, 'compta/validate_polymedia.html', locals())