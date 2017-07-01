from django import forms


class CreateAccountForm(forms.Form):
	"""this class creates a forms that gets the
	required infos to create a user"""
	nom = forms.CharField(max_length = 100, label = "Nom")
	prenom = forms.CharField(max_length = 100, label = "Prénom")
	login = forms.CharField(max_length = 100, label = "Login prenom.nom")
	password1 = forms.CharField(label = "Mot de passe",  widget=forms.PasswordInput)
	password2 = forms.CharField(label = "Confirmez le mot de passe",  widget=forms.PasswordInput)
