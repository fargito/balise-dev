from django import forms
from .models import Mandat, Binet
from django.contrib.auth.models import User


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

	def clean(self):
		cleaned_data = super(BinetCreateForm, self).clean()
		if len(Binet.objects.filter(nom=cleaned_data['nom'])) == 1:
			msg = 'Un binet avec ce nom existe déjà'
			self.add_error('nom', msg)


class MandatCreateForm(forms.ModelForm):
	"""permet de créer le premier mandat lors de la création d'un binet"""
	president = forms.ModelChoiceField(queryset=User.objects.order_by('username'))
	tresorier = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

	class Meta:
		model = Mandat
		fields = ('type_binet', 'president', 'tresorier', 'promotion')

	def clean(self):
		cleaned_data = super(MandatCreateForm, self).clean()
		print(self.data)
		print(cleaned_data)
		promotion = cleaned_data['promotion']
		tresorier = cleaned_data['tresorier']
		president = cleaned_data['president']
		# pour le cas du président inconnu, on vérifie pas la promo
		if president != User.objects.get(username='Inconnu') and tresorier != User.objects.get(username='Inconnu'):
			if promotion != president.eleve.promotion or promotion != tresorier.eleve.promotion or president.eleve.promotion != tresorier.eleve.promotion:
				msg = 'Incohérence entre la promotion et les promotions des membres'
				self.add_error('president', msg)



class MandatEditForm(forms.ModelForm):
	"""permet de modifier le mandat"""
	president = forms.ModelChoiceField(queryset=User.objects.order_by('username'))
	tresorier = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

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
		promotion = cleaned_data['promotion']
		tresorier = cleaned_data['tresorier']
		president = cleaned_data['president']
		# pour le cas du président inconnu, on vérifie pas la promo
		if president != User.objects.get(username='Inconnu') and tresorier != User.objects.get(username='Inconnu'):
			if promotion != president.eleve.promotion or promotion != tresorier.eleve.promotion or president.eleve.promotion != tresorier.eleve.promotion:
				msg = 'Incohérence entre la promotion et les promotions des membres'
				self.add_error('president', msg)

		if self.create and len(Mandat.objects.filter(binet=self.binet, promotion=promotion)) == 1:
			msg = 'Le mandat {} du binet {} existe déjà'.format(str(promotion), str(self.binet))
			self.add_error('promotion', msg)