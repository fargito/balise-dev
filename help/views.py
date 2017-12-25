from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, Http404


@login_required
def help_home(request):
	"""home to the help module"""
	return render(request, 'help/help_home.html', locals())


@login_required
def open_file(request, filename):
	"""permet d'ouvrir via leur nom tous les fichiers pdf contenus dans help/guides"""
	path = "help/guides/" + filename + ".pdf"

	try:
		return FileResponse(open(path, 'rb'), content_type='application/pdf')
	except FileNotFoundError:
		raise Http404()