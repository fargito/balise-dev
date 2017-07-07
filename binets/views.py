from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Binet, Mandat

def all_binets(request):
	"""sur cette page on peut accéder à la liste des binets
	actifs avec les responsables"""
	liste_binets = Binet.objects.filter(is_active=True)
	return render(request, 'binets/all_binets.html', locals())


def binet_set(request, id_binet):
	"""the only purpose of this view is to set the binet.
	It then redirects to the interesting view"""
	request.session['id_binet'] = id_binet
	# Here we have to check if the user can have this info
	return redirect('.')


def binet_history(request):
	"""generates the view for the binet history"""
	binet = Binet.objects.get(
		id=request.session['id_binet'])
	liste_mandats = Mandat.objects.filter(
		binet=binet)
	return render(request, 'binets/binet_history.html', locals())