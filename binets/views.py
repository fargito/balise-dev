from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Binet, Mandat

def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	actifs avec les responsables"""
	liste_binets = Binet.objects.all()
	return render(request, 'binets/all_binets.html', locals())



def binet_history(request, id_binet):
	"""generates the view for the binet history"""
	binet = Binet.objects.get(
		id=id_binet)
	liste_mandats = Mandat.objects.filter(
		binet=binet)
	return render(request, 'binets/binet_history.html', locals())