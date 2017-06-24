#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    """ Exemple de page HTML, non valide pour que l'exemple soit concis """

    text = """<h1>Bienvenue sur mon blog !</h1>

              <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>"""

    return HttpResponse(text)

def view_article(request, id_article):
	"""affiche un article selon son id"""
	return HttpResponse(

        "Vous avez demandé l'article #{0} !".format(id_article)    

    )