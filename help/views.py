from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


def help_home(request):
	"""home to the help module"""
	return render(request, 'help/help_home.html', locals())