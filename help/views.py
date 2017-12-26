from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, Http404
from django.db.models import Q

from django.forms import formset_factory, inlineformset_factory

from django.conf import settings
import os

from .models import HelpArticle, HelpParagraph
from .forms import HelpArticleForm, ImportFileForm, HelpParagraphForm

from django.core.files import File

from imports.file_handlers import file_handler


@login_required
def help_home(request):
	"""home to the help module
	Here we get all the HelpArticle to which the user is authorized to access
	and display it with a search field"""
	search_arguments = request.GET.get('q', None)

	if search_arguments:
		# on transfome la chaine brute en liste pour traiter séparément les mots
		search_arguments_list = search_arguments.split()
		# on construit une liste d'argments Q
		search_list = [Q(Q(title__icontains=q) |
			Q(subtitle__icontains=q)
			) for q in search_arguments_list]
		# on concatène ces arguments
		search = search_list.pop()
		for item in search_list:
			search |= item

		articles = HelpArticle.objects.filter(search)


	else:
		articles = HelpArticle.objects.all() #pour l'instant tout le monde a accès à tout

	return render(request, 'help/help_home.html', locals())


@login_required
def open_file(request, filename):
	"""permet d'ouvrir via leur nom tous les fichiers pdf contenus dans help/guides"""
	path = "help/guides/" + filename + ".pdf"

	try:
		return FileResponse(open(path, 'rb'), content_type='application/pdf')
	except FileNotFoundError:
		raise Http404()


@login_required
def help_article(request, article_id):
	"""affiche l'article"""
	# on commence par essayer de récupérer l'article dans la base de données. Si il n'existe pas on retourne 404
	try:
		article = HelpArticle.objects.get(id=article_id)
	except KeyError:
		raise Http404()

	if article.is_pdf:
		# dans ce cas on retourne le lien vers la vue pour les pdf
		return redirect(article.get_pdf_url())


	else:
		raise Http404()


@permission_required('help.add_helparticle')
def add_article(request):
	"""donne la page de choix qui propose d'importer un pdf ou de remplir un article à la main directement sur le site"""
	return render(request, 'help/choose_add.html')


@permission_required('help.add_helparticle')
def add_pdf_article(request):
	"""donne la page d'import d'un fichier pdf en tant qu'article. Création de l'objet HelpArticle et import
	du fichier correspondant dans le répertoire help/guides"""
	help_article_form = HelpArticleForm(request.POST or None)

	if request.method == 'POST':
		import_file_form = ImportFileForm(request.POST, request.FILES)
		if help_article_form.is_valid() and import_file_form.is_valid():
			# on doit récupérer le nom du fichier pour le mettre dans l'objet HelpArticle
			pdf_file = import_file_form.cleaned_data['pdf_file']
			filename = pdf_file.name.strip('.pdf')

			article = help_article_form.save(commit=False)
			article.is_pdf = True
			article.filename = filename

			# on attend d'avoir bien sauvegardé le fichier en mémoire avant d'enregistrer le HelpArticle
			pathname = 'help/guides/'+filename+'.pdf'
			file_handler(pdf_file, pathname)
			article.save()

			return redirect('help_home')

	else:
		import_file_form = ImportFileForm()

	return render(request, 'help/create_pdf_article.html', locals())


@permission_required('help.add_helparticle')
def add_html_article(request):
	help_article_form = HelpArticleForm(request.POST or None)
	if request.method == 'POST':
		"on a déjà fait une entrée"
		

	else:
		extra = 0


	return


@permission_required('help.add_helparticle')
def delete_article(request, article_id):
	"""permet de détruire un HelpArticle en prenant en compte que s'il est de type pdf if faut supprimer le
	pdf de help/guides/"""
	try:
		article = HelpArticle.objects.get(id=article_id)
	except KeyError:
		raise Http404()

	next = request.GET.get('next', 'help_home')

	if article.is_pdf:
		# on récupère le  lien vers le fichier
		pathname = settings.BASE_DIR + '/help/guides/' + article.filename + '.pdf'
		try:
			os.remove(pathname)
		except FileNotFoundError:
			pass

	article.delete()

	return redirect(next)