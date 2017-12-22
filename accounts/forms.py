from django import forms
from .models import Eleve
from django.contrib.auth.models import User

# les deux formulaires qui suivent sont appelés à la suite
# et servent aux nouveaux utilisateurs à s'enregistrer


class CreateAccountForm(forms.ModelForm):
	"""this class creates a forms that gets the
	required infos to create a Eleve. Its fields are based
	on the fields of Eleve"""

	class Meta:
		model = Eleve
		exclude = ('user', 'all_binets_passed', 'other_problem_circuitdepart', 'signed_fiche',)
		labels = {'prenom': 'Prénom'}



class CreateUserForm(forms.Form):
	"""is used to create the get the infos for the user"""

	username = forms.CharField(label="Identifiant prenom.nom")
	password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirmez mot de passe", widget=forms.PasswordInput)
	
	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password1 != password2:
			raise forms.ValidationError("Les mots de passe ne correspondent pas")


class CreateUserWithoutPwdForm(forms.Form):
	"""is used to create a local user without local password (only through Frankiz)"""
	username = forms.CharField(label="Identifiant prenom.nom")

	def clean(self):
		cleaned_data = super(CreateUserWithoutPwdForm, self).clean()
		# if len(User.objects.filter(username=cleaned_data["username"])) == 1:
		# 	msg = "Cet identifiant est déjà utilisé"
		# 	self.add_error("username", msg)