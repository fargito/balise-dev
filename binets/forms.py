from django import forms
from .models import Mandat, Binet

class DescriptionForm(forms.ModelForm):
	"""defines a form to get the description of a mandat. It is called in the 'Remarques binet' module of the compta module"""
	
	class Meta:
		model = Mandat
		fields = ('description',)
		labels = {'description': 'Commentaires généraux sur votre mandat'}


class BinetEditForm(forms.ModelForm):
	"""permet de modifier les binets"""

	class Meta:
		model = Binet
		exclude = ('creator',)
		labels = {'description': 'Description du binet (visible par tous, non modifiable par les membres)',
			 'remarques_admins': 'Remarques générales sur le binet (visibles par les kessiers seulement)'}


class BinetCreateForm(forms.ModelForm):
	"""permet de créer un binet avec un permier mandat"""
	class Meta:
		model = Binet
		exclude = ('creator',)


class MandatEditForm(forms.ModelForm):
	"""permet de modifier le mandat"""

	def __init__(self, binet, create, *args, **kwargs):
		super(MandatEditForm, self).__init__(*args, **kwargs)
		self.binet = binet
		self.create = create

	class Meta:
		model = Mandat
		exclude = ('binet', 'creator',)
		labels = {'description': 'Description du mandat (visible et modifiable par les membres)',
			 'remarques_admins': 'Remarques générales sur le mandat (visibles par les kessiers seulement)'}


	def clean(self):
		cleaned_data = super(MandatEditForm, self).clean()
		print(cleaned_data)
		promotion = cleaned_data['promotion']
		tresorier = cleaned_data['tresorier']
		president = cleaned_data['president']
		if promotion != president.eleve.promotion or promotion != tresorier.eleve.promotion or president.eleve.promotion != tresorier.eleve.promotion:
			msg = 'Incohérence entre la promotion et les promotions des membres'
			self.add_error('president', msg)

		if self.create and len(Mandat.objects.filter(binet=self.binet, promotion=promotion)) == 1:
			msg = 'Le mandat {} du binet {} existe déjà'.format(str(promotion), str(self.binet))
			self.add_error('promotion', msg)