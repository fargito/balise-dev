from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from blog.models import Article
# Il faut ajouter l'import get_object_or_404, attention !
from django.shortcuts import render, get_object_or_404
from .forms import ContactForm, ArticleForm


# Create your views here.

def home(request):

    return render(request, 'blog/home.html')



def date_actuelle(request):

    return render(request, 'blog/date.html', {'date': datetime.now()})



def addition(request, nombre1, nombre2):    

    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl

    return render(request, 'blog/addition.html', locals())




def accueil(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    return render(request, 'blog/accueil.html', {'derniers_articles': articles})

def lire(request, id, slug):

    article = get_object_or_404(Article, id=id, slug = slug)

    return render(request, 'blog/lire.html', {'article':article})



def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']
        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/contact.html', locals())

def article_form(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']
        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    return render(request, 'blog/article_form.html', locals())