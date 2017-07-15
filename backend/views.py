from django.shortcuts import render
from django.http import HttpResponseRedirect
from imports.forms import ImportFileForm
from django.contrib.auth.decorators import permission_required
from imports.file_handlers import eleves_file_handler, binets_file_handler, subventions_file_handler
from imports.file_handlers import create_eleves, create_binets, create_subventions
from .forms import VagueForm
import pandas, os
from datetime import datetime



@permission_required('is_staff')
def backend_home(request):
	"""is only accessible to the kessiers"""
	return render(request, 'backend/backend_home.html')


@permission_required('is_staff')
def import_eleves(request):
	"""permet d'importer un fichier excel contenant
	une liste d'eleves et la crée dans la base de données"""
	pathname = 'imports/logs/eleves_imports/names.xls'
	if request.method == 'POST':
		if request.POST['validation'] == 'Upload':
			# l'utilisateur a appuyé sur le bouton upload
			import_form = ImportFileForm(request.POST, request.FILES)
			if import_form.is_valid():
				# on copie l'import en mémoire
				eleves_file_handler(request.FILES['excel_file'], pathname)
				# on redirige vers la validation
				sent = False
				# on lit les données importées et on les met dans un dict
				imported_eleves = pandas.read_excel(open(pathname, 'rb'), sheetname=0)
				imported_eleves = imported_eleves.transpose().to_dict().values()
				# On affiche les élèves
				imported_eleves_list = []
				for eleve in imported_eleves:
					# on accepte que les identifiants soient mis en adresse mail polytechnique
					# dans ce cas on effectue le traitement nécessaire
					if '@polytechnique.edu' in eleve['Identifiant']:
						eleve['Identifiant'] = eleve['Identifiant'].split(
							'@polytechnique.edu')[0]
					imported_eleves_list.append([eleve['Nom'], eleve['Prénom'],
					 eleve['Promotion'], eleve['Identifiant']])
				return render(request, 'backend/confirm_import_eleves.html', locals())
		else:
			if request.POST['validation'] == 'Valider':
				# dans ce cas on crée les objets élèves correspondants
				imported_eleves = pandas.read_excel(open(pathname, 'rb'), sheetname=0)
				imported_eleves = imported_eleves.transpose().to_dict().values()
				create_eleves(request, imported_eleves)
				# on supprime le fichier temporaire
				os.remove(pathname)
				sent = True
			else:
				# on supprime le fichier temporaire
				os.remove(pathname)
				sent = True
				request.session['messages'] = 'Requête annulée'
				print('on annule tout')

			return render(request, 'backend/confirm_import_eleves.html', locals())
	else:
		import_form = ImportFileForm()
	return render(request, 'backend/import_eleves.html', locals())


	

@permission_required('is_staff')
def import_binets(request):
	"""permet d'importer une liste de binets, avec leurs
	président et trésoriers actuels. Si le binet existe déjà,
	"""
	if request.method == 'POST':
		if request.POST['validation'] == 'Upload':
			# l'utilisateur a appuyé sur le bouton upload
			import_form = ImportFileForm(request.POST, request.FILES)
			if import_form.is_valid():
				# on copie l'import en mémoire
				date = datetime.today()
				pathname = 'imports/logs/binets_imports/import_binets_'+str(date.year)+'_'+\
					str(date.month)+'_'+str(date.day)+' '+str(
					date.hour)+'_'+str(date.minute)
				request.session['pathname'] = pathname
				binets_file_handler(request.FILES['excel_file'], pathname)
				# on redirige vers la validation
				sent = False
				# on lit les données importées et on les met dans un dict
				imported_binets = pandas.read_excel(open(pathname, 'rb'), sheetname=0)
				imported_binets = imported_binets.transpose().to_dict().values()
				# On affiche les binets
				imported_binets_list = []
				for binet in imported_binets:
					# on accepte que les identifiants soient mis en adresse mail polytechnique
					# dans ce cas on effectue le traitement nécessaire
					if '@polytechnique.edu' in binet['Président']:
						binet['Président'] = binet['Président'].split(
							'@polytechnique.edu')[0]
					if '@polytechnique.edu' in binet['Trésorier']:
						binet['Trésorier'] = binet['Trésorier'].split(
							'@polytechnique.edu')[0]
					imported_binets_list.append(
						(binet['Binet'], binet['Type'], binet['Promotion'],
						binet['Président'], binet['Trésorier']))
				request.session['messages'] = []
				request.session['messages'].append('Copied the file in the database')
				return render(request, 'backend/confirm_import_binets.html', locals())
		else:
			if request.POST['validation'] == 'Valider':
				# dans ce cas on crée les objets élèves correspondants
				imported_binets = pandas.read_excel(open(request.session[
					'pathname'], 'rb'), sheetname=0)
				imported_binets = imported_binets.transpose().to_dict().values()
				create_binets(request, imported_binets)
				# on supprime le fichier temporaire
				del request.session['pathname']
				sent = True
			else:
				# on supprime le fichier temporaire
				del request.session['pathname']
				request.session['messages'] = ['Requête annulée']
				sent = True
				print('on annule tout')

			return render(request, 'backend/confirm_import_binets.html', locals())
	else:
		import_form = ImportFileForm()
	return render(request, 'backend/import_binets.html', locals())





@permission_required('is_staff')
def import_subventions(request):
	"""permet d'importer une vague de subventions
	une vague de subventions ne peut être remplie qu'une fois.
	Si il y a des erreurs, modifier au cas par cas dans l'interface
	admin django ou supprimer complètement la vague et la réimporter"""
	if request.method == 'POST':
		if request.POST['validation'] == 'Upload':
			# l'utilisateur a appuyé sur le bouton upload
			vague_form = VagueForm(request.POST)
			import_form = ImportFileForm(request.POST, request.FILES)
			# on commence par tester si la vague de subventions n'a pas été remplie
			if vague_form.is_valid():
				# vague_subventions = vague_form.save(commit=False)
				if import_form.is_valid():
					# on rentre les infos sur la vague de subventions et le chemin du
					# fichier pour pouvoir les créer plus tard
					request.session['vague_annee'] = vague_form.cleaned_data['annee']
					request.session['vague_type'] = str(vague_form.cleaned_data['type_subvention'])
					# on copie l'import en mémoire
					date = datetime.today()
					pathname = 'imports/logs/subventions_imports/'+request.session[
						'vague_annee']+str(vague_form.cleaned_data['type_subvention'])
					
					request.session['pathname'] = pathname
					# on enregistre le fichier temporaire
					binets_file_handler(request.FILES['excel_file'], pathname)
					# on redirige vers la validation
					sent = False
					# on lit les données importées et on les met dans un dict
					imported_subventions = pandas.read_excel(open(pathname, 'rb'), sheetname=0)
					imported_subventions = imported_subventions.transpose().to_dict().values()
					# On affiche les binets
					imported_subventions_list = []
					for subvention in imported_subventions:
						# on accepte que les identifiants soient mis en adresse mail polytechnique
						# dans ce cas on effectue le traitement nécessaire
						imported_subventions_list.append(
							(subvention['Binet'], subvention['Promotion'],subvention['Demandé'], subvention['Accordé'],
							subvention['Postes']))
					request.session['messages'] = []
					request.session['messages'].append('Copied the file in the database')
					return render(request, 'backend/confirm_import_subventions.html', locals())

		else:
			if request.POST['validation'] == 'Valider':
				# dans ce cas on crée les objets élèves correspondants
				imported_subventions = pandas.read_excel(open(request.session[
					'pathname'], 'rb'), sheetname=0)
				imported_subventions = imported_subventions.transpose().to_dict().values()
				create_subventions(request, imported_subventions)
				# on supprime le fichier temporaire
				del request.session['pathname']
				sent = True
			else:
				# on supprime le fichier temporaire
				del request.session['pathname']
				request.session['messages'] = ['Requête annulée']
				sent = True
				print('on annule tout')

			return render(request, 'backend/confirm_import_binets.html', locals())
	else:
		vague_form = VagueForm()
		import_form = ImportFileForm()
	return render(request, 'backend/import_subventions.html', locals())