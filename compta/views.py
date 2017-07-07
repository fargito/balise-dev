#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from binets.models import Mandat
from django.db.models import Q


@login_required
def my_binets(request):
	"""this page allows the user to select the binets
	in which he has a role. If he's admin, he can have them all.
	This views allows the user to place a Binet object in the session.
	It will be implied in the compta module that this Object is in
	th session parameters"""

	if request.user.is_staff:
		liste_mandats = Mandat.objects.all()

	else:
		liste_mandats = Mandat.objects.filter(
			Q(president=request.user) | 
			Q(tresorier=request.user))

	return render(request, 'compta/my_binets.html', locals())


def mandat_set(request, id_mandat):
	"""this function's only purpose is to set
	the session variable to id and then redirect to
	mandat_journal"""
	request.session['id_mandat'] = id_mandat
	# Here we have to check if the user can have this info
	return redirect('.')

def mandat_journal(request):
	"""affiche le journal comptable et permet de le modifier"""
	return render('')