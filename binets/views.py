from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Binet

def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	avec les responsables"""
	liste_binets = Binet.objects.all()
	print(liste_binets)
	return render(request, 'binets/all_binets.html')
