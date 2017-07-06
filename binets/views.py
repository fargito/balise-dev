from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Binet

def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	actifs avec les responsables"""
	liste_binets = Binet.objects.filter(is_active=True)
	return render(request, 'binets/all_binets.html', locals())
