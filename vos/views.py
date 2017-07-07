#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from vos.models import Participation, MontantCheque, Encaissement, EleveVos, VOS
from django.db.models import Q
from .forms import participationForm




@login_required
def home(request):
	"""home page for the vos section"""

	#temporaire
	liste_vos = VOS.objects.filter(is_active=True)
	vos_var = liste_vos[0]
	promo = vos_var.current_promotion

	liste_cheques = MontantCheque.objects.filter(
			evenement=vos_var, 
			promotion=promo
			).order_by('ordre')
	
	liste_participants = Participation.objects.filter(
			evenement=vos_var, 
			promotion=promo
			).order_by('eleve')

	return render(request, "vos/home.html", locals())

@login_required
def participants(request):
	"""home page for the vos section"""

	#temporaire
	liste_vos = VOS.objects.filter(is_active=True)
	vos_var = liste_vos[0]
	promo = vos_var.current_promotion
	
	liste_section = EleveVos.objects.filter(
			promotion=promo,
			section = vos_var.section
			).order_by('promotion','nom','prenom')

	participe=dict()
	for p in liste_section:
		requete = Participation.objects.filter(
			eleve=p,
			evenement=vos_var,
			promotion=promo)
		participe[p.id]=(len(requete)>0) and ((requete[0]).participation)
			

	form = participationForm(request.POST or None)

	return render(request, "vos/participants.html", locals())

