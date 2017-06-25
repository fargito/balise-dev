#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ConnexionForm
from django.core.urlresolvers import reverse

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            print("form is valid")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect(reverse(home))
            else: # sinon une erreur sera affichée
                error = True

    else:
        form = ConnexionForm()

    return render(request, 'compta/connexion.html', locals())

def deconnexion(request):
	logout(request)
	return redirect(reverse(connexion))



@login_required
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