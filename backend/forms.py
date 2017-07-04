from django import forms
from .models import ValidateEleve

# obsolete
class ValidateEleveForm(forms.ModelForm):
	"""this class creates a forms to confirm the
	creation of eleves. Its fields are based
	on the fields of ValidateEleve"""

	class Meta:
		fields='__all__'
		model = ValidateEleve
		labels = {'prenom': 'Prénom'}