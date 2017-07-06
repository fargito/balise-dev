#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse




@login_required
def home(request):
	"""home page for the vos section"""
	return render(request, "vos/home.html")

