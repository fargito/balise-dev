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
from imports.forms import ImportFileForm

from imports.file_handlers import file_handler, create_lignes_compta

from subventions.helpers import generate_ordering_arguments, generate_ordering_links

from datetime import datetime
import pandas


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
	mandat_journal, or to the optional 'next' parameter"""
	request.session['id_mandat'] = id_mandat
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

	else:
		request.session['edit'] = False


	# ici on récupère les lignes du mandat, en les ordonnant selon les filtres donnés
	# ces filtres sont donnés par ordre dans la liste d'attributs donnée
	# ces attribut n'incluent pas les subventions, qu'on peut isoler dans la partie subventions

	


	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	attributes = ['date', 'description', 'debit', 'credit']
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

				return redirect('../')
				

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
				# On affiche les binets
				imported_lignes_list = []
				for ligne in imported_lignes:
					# si les imports sont en nan, on les transforme en None
					if not float(ligne['Débit']) > 0:
						ligne['Débit'] = None
					if not float(ligne['Crédit']) > 0:
						ligne['Crédit'] = None
					imported_lignes_list.append(
						(ligne['Date'], ligne['Description'], ligne['Débit'], ligne['Crédit']))
				request.session['messages'] = []
				request.session['messages'].append('Copied the file in the database')

				return render(request, 'compta/import_lignes_confirm.html', locals())
		else:
			if request.POST['validation'] == 'Valider':
				imported_lignes = pandas.read_excel(open(request.session[
					'pathname'], 'rb'), sheetname=0, na_values = ['-'])
				imported_lignes = imported_lignes.transpose().to_dict().values()
				create_lignes_compta(request, imported_lignes, mandat)
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