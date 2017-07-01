from django.shortcuts import render
from .forms import CreateAccountForm


def home(request):
	"""caution the home view is defined here"""
	return render(request, 'welcome.html')


def create_account(request):
	"""users can register here to create an account.
	At first it is linked with no Binet"""
	sent = False
	form = CreateAccountForm(request.POST or None)
	if form.is_valid():
		#to be changed
		username = form.cleaned_data["nom"]
		password = form.cleaned_data["password1"]
			
		print(username, password)
		sent = True
	return render(request, 'accounts/create_account.html', locals())