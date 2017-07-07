from django.forms import ModelForm
from .models import Participation
from django.utils.translation import ugettext_lazy as _

class participationForm(ModelForm):
	class Meta:
		model = Participation
		fields = ['participation']
		labels = {
			'participation': _(''),
		}
