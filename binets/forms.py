from django import forms
from .models import Mandat

class DescriptionForm(forms.ModelForm):
	"""defines a form to get the description of a mandat. It is called in the 'Remarques binet' module of this module"""
	
	class Meta:
		model = Mandat
		fields = ('description',)
		labels = {'description': 'Commentaires généraux sur votre mandat'}


class SearchForm(forms.Form):
	"""permet de rechercher les binets par nom"""
	search = forms.CharField(max_length=100, label="Rechercher", required=False)