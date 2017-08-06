from django import forms
from .models import Mandat, Binet

class DescriptionForm(forms.ModelForm):
	"""defines a form to get the description of a mandat. It is called in the 'Remarques binet' module of the compta module"""
	
	class Meta:
		model = Mandat
		fields = ('description',)
		labels = {'description': 'Commentaires généraux sur votre mandat'}


class SearchForm(forms.Form):
	"""permet de rechercher les binets par nom"""
	search = forms.CharField(max_length=100, label="Rechercher", required=False)


class BinetEditForm(forms.ModelForm):
	"""permet de modifier les binets"""

	class Meta:
		model = Binet
		exclude = ('creator', 'current_promotion')
		labels = {'description': 'Description du binet (non modifiable par les membres)',
			 'remarques_admins': 'Remarques générales sur le binet (pour les kessiers seulement)'}


class MandatEditForm(forms.ModelForm):
	"""permet de modifier le mandat"""

	class Meta:
		model = Mandat
		exclude = ('binet', 'creator', 'passed_date')
		labels = {'description': 'Description du mandat (modifiable par les membres)',
			 'remarques_admins': 'Remarques générales sur le mandat (pour les kessiers seulement)'}
