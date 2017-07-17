from django import forms
from .models import ValidateEleve
from subventions.models import VagueSubventions

# obsolete
class ValidateEleveForm(forms.ModelForm):
	"""this class creates a forms to confirm the
	creation of eleves. Its fields are based
	on the fields of ValidateEleve"""

	class Meta:
		fields='__all__'
		model = ValidateEleve
		labels = {'prenom': 'Prénom'}



class VagueForm(forms.ModelForm):
	"""allows the admin to create the VagueSubvention
	object when importing a subvention vague"""

	class Meta:
		model = VagueSubventions
		fields = '__all__'
		labels = {'type_subvention': 'Vague de subventions'}