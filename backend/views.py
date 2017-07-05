from django.shortcuts import render
from django.http import HttpResponseRedirect
from imports.forms import ImportFileForm
from django.contrib.auth.decorators import permission_required
from imports.file_handlers import eleves_file_handler, binets_file_handler
from imports.file_handlers import create_eleves, create_binets
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
				validated = False
				sent = False
				# on lit les données importées et on les met dans un dict
				imported_eleves = pandas.read_excel(open(pathname, 'rb'), sheetname=0)
				imported_eleves = imported_eleves.transpose().to_dict().values()
				# On affiche les élèves
				imported_eleves_html = []
				for eleve in imported_eleves:
					# on accepte que les identifiants soient mis en adresse mail polytechnique
					# dans ce cas on effectue le traitement nécessaire
					if '@polytechnique.edu' in eleve['Identifiant']:
						eleve['Identifiant'] = eleve['Identifiant'].split(
							'@polytechnique.edu')[0]
					imported_eleves_html.append(
						'<div class="nom">{}</div><div class="prenom">\
						 {}</div class="promo"X{} ,</div><div class="id">\
						 identifiant: {}</div>'.format(eleve['Nom'],
							eleve['Prénom'], eleve['Promotion'], eleve['Identifiant']))
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
				validated = True
			else:
				# on supprime le fichier temporaire
				os.remove(pathname)
				sent = True
				validated = False
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
				del request.session['message']
				request.session['message'] = []
				request.session['message'].append('Copied the file in the database')
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
				del request.session['message']
				request.session['message'].append('Requête annulée')
				sent = True
				print('on annule tout')

			return render(request, 'backend/confirm_import_binets.html', locals())
	else:
		import_form = ImportFileForm()
	return render(request, 'backend/import_binets.html', locals())