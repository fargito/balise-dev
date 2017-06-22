#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    """ Exemple de page HTML, non valide pour que l'exemple soit concis """

    text = """<h1>Bienvenue sur mon blog !</h1>

              <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>"""

    return HttpResponse(text)
