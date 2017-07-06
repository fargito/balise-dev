#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from vos.models import Participation, MontantCheque, Encaissement, EleveVos, VOS
from django.db.models import Q




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
	return render(request, "vos/home.html", locals())

