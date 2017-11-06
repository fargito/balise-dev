from django import forms
from accounts.models import Promotion
from .models import Mandat, Binet, TagBinet, TypeBinet
from django.contrib.auth.models import User


class DescriptionForm(forms.ModelForm):
	"""defines a form to get the description of a mandat. It is called in the 'Remarques binet' module of the compta module"""
	
	class Meta:
		model = Mandat
		fields = ('description',)
		labels = {'description': 'Commentaires généraux sur votre mandat'}


class BinetEditForm(forms.ModelForm):
	"""permet de modifier les binets"""
	tag_binet = forms.ModelMultipleChoiceField(queryset=TagBinet.objects.all(), required=False, label='Catégories')

	class Meta:
		model = Binet
		exclude = ('creator',)
		labels = {'description': 'Description du binet (visible par tous, non modifiable par les membres)',
			 'remarques_admins': 'Remarques générales sur le binet (visibles par les kessiers seulement)'}


class BinetCreateForm(forms.ModelForm):
	"""permet de créer un binet avec un permier mandat"""
	tag_binet = forms.ModelMultipleChoiceField(queryset=TagBinet.objects.all(), required=False, label='Catégories')

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
	president = forms.ModelChoiceField(queryset=User.objects.filter(eleve__signed_fiche=False).order_by('username'))
	tresorier = forms.ModelChoiceField(queryset=User.objects.filter(eleve__signed_fiche=False).order_by('username'))

	class Meta:
		model = Mandat
		fields = ('type_binet', 'president', 'tresorier', 'promotion')

	def clean(self):
		cleaned_data = super(MandatCreateForm, self).clean()
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
	president = forms.ModelChoiceField(queryset=User.objects.filter(eleve__signed_fiche=False).order_by('username'))
	tresorier = forms.ModelChoiceField(queryset=User.objects.filter(eleve__signed_fiche=False).order_by('username'))

	def __init__(self, binet, create, *args, **kwargs):
		super(MandatEditForm, self).__init__(*args, **kwargs)
		self.binet = binet
		self.create = create

	class Meta:
		model = Mandat
		exclude = ('binet', 'creator', 'is_last', 'create_date', 'is_active', 'being_checked')
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


class PassationMandatForm(forms.ModelForm):
	"""permet de créer un formulaire de description et remarques_admins lors de la passation"""

	class Meta:
		model = Mandat
		fields = ('description', 'remarques_admins')
		labels = {'description': 'Remarques sur le mandat visibles par les membres du binet :',
					'remarques_admins': 'Remarques pour les kessiers :'}


class SearchBinetForm(forms.Form):
	binet = forms.CharField(required=False)
	promotion = forms.ModelMultipleChoiceField(queryset=Promotion.objects.all(), required=False)
	type_binet = forms.ModelMultipleChoiceField(queryset=TypeBinet.objects.all(), required=False)
	categorie = forms.ModelMultipleChoiceField(queryset=TagBinet.objects.all(), required=False, label='Catégories')
	active_only = forms.BooleanField(initial=False, required=False, label='Mandats actifs uniquement')
	is_last_only = forms.BooleanField(initial=True, required=False, label='Plus récents uniquement')
	public_only = forms.BooleanField(initial=True, required=False, label='Publics uniquement')