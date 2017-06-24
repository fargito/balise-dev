from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

# Create your views here.

def home(request):

    """ Exemple de page HTML, non valide pour que l'exemple soit concis """

    text = """<h1>Bienvenue sur mon blog !</h1>

              <p>Les crêpes bretonnes ça tue des mouettes en plein vol ! Sauf qu'ici on est sur le module blog</p>"""

    return HttpResponse(text)

def date_actuelle(request):

    return render(request, 'blog/date.html', {'date': datetime.now()})



def addition(request, nombre1, nombre2):    

    total = int(nombre1) + int(nombre2)


    # Retourne nombre1, nombre2 et la somme des deux au tpl

    return render(request, 'blog/addition.html', locals())
