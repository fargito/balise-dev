from django.shortcuts import render
from .forms import CreateAccountForm, CreateUserForm
from django.contrib.auth.models import User
from .models import Eleve


def home(request):
	"""caution the home view is defined here"""
	return render(request, 'welcome.html')


def create_account(request):
	"""users can register here to create an account.
	At first it is linked with no Binet"""
	sent = False
	user_form = CreateUserForm(request.POST or None)
	account_form = CreateAccountForm(request.POST or None)
	if (account_form.is_valid() and user_form.is_valid()):
		# on récupère les données du formulaire
		username = user_form.cleaned_data['username']
		password = user_form.cleaned_data['password1']
		email = username+'@polytechnique.edu'
		user = User.objects.create_user(username, 
			email, password)
		eleve = account_form.save(commit = False)
		eleve.user = user
		eleve.save()

		# Dans ce cas, on crée un profil utilisateur




		print("User profile created")
		sent = True
	return render(request, 'accounts/create_account.html', locals())