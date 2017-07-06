#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from binets.models import Binet
from django.db.models import Q


@login_required
def my_binets(request):
	"""this page allows the user to select the binets
	in which he has a role. If he's admin, he can have them all.
	This views allows the user to place a Binet object in the session.
	It will be implied in the compta module that this Object is in
	th session parameters"""
	if request.user.is_staff:
		liste_binets = Binet.objects.all()
	else:
		liste_binets = Binet.objects.filter(
			Q(current_president=request.user) | 
			Q(current_tresorier=request.user))
	return render(request, 'compta/my_binets.html', locals())