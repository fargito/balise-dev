from django.shortcuts import render
from django.http import HttpResponseRedirect
from imports.forms import ImportFileForm
from django.contrib.auth.decorators import permission_required
from imports.file_handlers.eleves_handler import eleves_file_handler
import pandas


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
	validated = request.method=='POST'
	imported_eleves = pandas.read_excel(open('imports/logs/eleves_imports/names.xls', 'rb'), sheetname=0)
	imported_eleves = imported_eleves.values.tolist()
	# On affiche les élèves
	imported_eleves_html = []
	for eleve in imported_eleves:
		imported_eleves_html.append(
			'<div class="nom">{}</div><div class="prenom">\
			 {}</div class="promo"X{} ,</div><div class="id">\
			 identifiant: {}</div>'.format(eleve[0],
				eleve[1], eleve[2], eleve[3]))
	if validated:
		# dans ce cas on crée les objets élèves correspondants
		print('on a validé les élèves')
	
	return render(request, 'backend/confirm_import_eleves.html', locals())