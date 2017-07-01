#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse




@login_required
def home(request):

    """ Exemple de page HTML, non valide pour que l'exemple soit concis """

    text = """<h1>Bienvenue sur la main page de compta !</h1>

              <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>"""

    return HttpResponse(text)


@login_required
def view_article(request, id_article):
	"""affiche un article selon son id"""
	return HttpResponse(

        "Vous avez demandé l'article #{0} !".format(id_article)    

    )