from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def help_home(request):
	"""home to the help module"""
	try:
		attributes = request.session['attributes']
	except:
		attributes = "pas d'attributes"
	return render(request, 'help/help_home.html', locals())