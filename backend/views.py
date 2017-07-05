from django.shortcuts import render
from django.http import HttpResponseRedirect
from imports.forms import ImportFileForm
from django.contrib.auth.decorators import permission_required
from imports.file_handlers.eleves_handler import eleves_file_handler
import pandas, os
from accounts.models import Eleve, Promotion
from django.contrib.auth.models import User


@permission_required('is_staff')
def backend_home(request):
	"""is only accessible to the kessiers"""
	return render(request, 'backend/backend_home.html')


@permission_required('is_staff')
def import_eleves(request):
	"""permet d'importer un fichier excel contenant
	une liste d'eleves et la crée dans la base de données"""
	if request.method == 'POST':
		import_form = ImportFileForm(request.POST, request.FILES)
		if import_form.is_valid():
			eleves_file_handler(request.FILES['excel_file'])
			# on redirige vers la validation
			return HttpResponseRedirect('./confirm')
	else:
		import_form = ImportFileForm()
	return render(request, 'backend/import_eleves.html', locals())


@permission_required('is_staff')
def confirm_import_eleves(request):
	"""is called after the import. The admin can validate its 
	imports"""
	validated = False
	sent = False
	imported_eleves = pandas.read_excel(open('imports/logs/eleves_imports/names.xls', 'rb'), sheetname=0)
	imported_eleves = imported_eleves.transpose().to_dict().values()
	# On affiche les élèves
	imported_eleves_html = []
	for eleve in imported_eleves:
		imported_eleves_html.append(
			'<div class="nom">{}</div><div class="prenom">\
			 {}</div class="promo"X{} ,</div><div class="id">\
			 identifiant: {}</div>'.format(eleve['Nom'],
				eleve['Prénom'], eleve['Promotion'], eleve['Identifiant']))
	if request.method=='POST':
		# l'utilisateur a appuyé sur un bouton
		if request.POST['validation'] == 'Valider':
			# dans ce cas on crée les objets élèves correspondants
			print('Creating or updating eleves:')
			for eleve in imported_eleves:
				# on accepte que les identifiants soient mis en adresse mail polytechnique
				# dans ce cas on effectue le traitement nécessaire
				if '@polytechnique.edu' in eleve['Identifiant']:
					eleve['Identifiant'] = eleve['Identifiant'].split(
						'@polytechnique.edu')[0]
				created_user, user_was_created = User.objects.update_or_create(
					username=eleve['Identifiant'],
					email=eleve['Identifiant']+'@polytechnique.edu')	
				if user_was_created:
					# on ne réinitialise pas les mots de passe si update seulement
					created_user.set_password(eleve['Mot de passe'])
				created_user.save()

				created_eleve, eleve_was_created = Eleve.objects.update_or_create(
					user=created_user, nom=eleve['Nom'],
					prenom=eleve['Prénom'], promotion=Promotion.objects.get(
						nom=eleve['Promotion']))
				created_eleve.save()
				affichage = {True:'Created: ', False:'Updated: '}
				print(affichage[user_was_created],created_user)
				# on supprime le fichier temporaire
			os.remove('imports/logs/eleves_imports/names.xls')
			sent = True
			validated = True
		else:
			# on supprime le fichier temporaire
			os.remove('imports/logs/eleves_imports/names.xls')
			sent = True
			validated = False
			print('on annule tout')
	
	return render(request, 'backend/confirm_import_eleves.html', locals())