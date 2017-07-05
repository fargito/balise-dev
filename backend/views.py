from django.shortcuts import render
from django.http import HttpResponseRedirect
from imports.forms import ImportFileForm
from django.contrib.auth.decorators import permission_required
from imports.file_handlers import eleves_file_handler, binets_file_handler, create_eleves
import pandas, os



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
				create_eleves(imported_eleves)
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


	


def import_binets(request):
	"""permet d'importer une liste de binets, avec leurs
	président et trésoriers actuels. Si le binet existe déjà,
	les noms du président et du trésorier ne sont pas actualisés"""
	return render("")