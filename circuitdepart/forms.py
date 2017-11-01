from django import forms
from .models import ProblemDepart
from django.contrib.auth.models import User


class ProblemDepartForm(forms.ModelForm):
	"""permet de rentrer un nouveau problème pour un utilisateur existant"""
	user = forms.ModelChoiceField(queryset=User.objects.order_by('username'))


	class Meta:
		model = ProblemDepart
		exclude = ('resolved',)