from django import forms
from django.db.models import Q
from .models import LigneCompta, PosteDepense
from subventions.models import DeblocageSubvention
from accounts.models import Promotion
from binets.models import Binet, Mandat
from django.forms import BaseFormSet, BaseInlineFormSet



class LigneComptaForm(forms.ModelForm):
	"""this form is used in the compta journal to enter
	a new compta opération or edit an existing one
	on définit à part le champ pour le poste de dépense pour pouvoir gérer les possessions de postes
	attentio il doit être défini avant l'instanciation du formulaire avec 

	LigneComptaForm.base_fields['poste_depense'] = forms.ModelChoiceField(
			queryset=PosteDepense.objects.filter(
				Q(mandat=mandat) | Q(mandat=None)), required=False, empty_label="Aucun")
	"""

	
	class Meta:
		model = LigneCompta
		exclude = ('mandat','auteur','modificateur', 'add_date', 'edit_date', 'is_locked')
		required = {'credit': False, 'debit': False, 'poste_depense': False}


	def clean(self):
		"""on définit la validation : les montants ne peuvent pas
		être négatifs, ni tous les deux nuls"""
		cleaned_data = super(LigneComptaForm, self).clean()
		debit = cleaned_data.get('debit')
		credit = cleaned_data.get('credit')
		
		if debit == None and credit == None:
			msg = "Les deux montants ne peuvent pas être nuls"
			self.add_error("debit", msg)
		elif debit == None or credit == None:
			if debit == 0.0 or credit == 0.0:
				msg = "Les deux montants ne peuvent pas être nuls"
				self.add_error("debit", msg)
		else:
			if ((debit == 0.0) and (credit == 0.0)):
				msg = "Les deux montants ne peuvent pas être nuls"
				self.add_error("debit", msg)
			if debit < 0 or credit < 0:
				msg = "Les montants doivent être positifs"
				self.add_error("debit", msg)
			if debit > 0 and credit > 0:
				msg = "Une opération de peut pas être débit et crédit"
				self.add_error("debit", msg)



class DeblocageSubventionForm(forms.ModelForm):
	"""définit un formulaire permettant de créer un déblocage de subventions sur une vague"""

	class Meta:
		model = DeblocageSubvention
		fields = ('montant',)

	def clean(self):
		"""on définit la validation pour le paramètre ne dépendant que du champ:
		il doit être positif"""
		cleaned_data = super(DeblocageSubventionForm, self).clean()
		montant = cleaned_data.get('montant')

		if montant and montant < 0:
			msg = 'Les montants débloqués doivent être positifs'
			self.add_error('montant', msg)



class BaseDeblocageSubventionFormSet(BaseFormSet):
	"""sert à définir les critères de validation groupés des subventions pour leur création"""

	def __init__(self, subventions_list, *args, **kwargs):
		"""on surcharge la méthode d'initialisation pour pouvoir transmettre au formset la liste des subventions utilisée"""
		self.subventions_list = subventions_list
		super(BaseDeblocageSubventionFormSet, self).__init__(*args, **kwargs)


	def clean(self):
		if any(self.errors):
			"""on se fait pas chier à valider le formset si un des formulaires a une erreur"""
			return

		if(self.data['credit'] and float(self.data['credit']) > 0):
			"""on ne peut pas subventionner une recette"""
			for deblocage in self.cleaned_data:
				try:
					if deblocage['montant'] and deblocage['montant'] > 0:
						raise forms.ValidationError("Impossible de débloquer des subventions sur une recette")
				except KeyError:
					pass

		somme_deblocages = 0
		for deblocage in self.cleaned_data:
			try:
				if deblocage['montant']:
					somme_deblocages += deblocage['montant']
			except KeyError:
				pass

		if(self.data['debit'] and float(self.data['debit']) < (somme_deblocages)):
			raise forms.ValidationError('Impossible de débloquer des subventions supérieures au montant de la dépense')

		for k in range(len(self.subventions_list)):
			subvention = self.subventions_list[k]
			deblocage = self.cleaned_data[k]
			try:
				if deblocage['montant'] > 0:
					if subvention.is_versee:
						# si la subvention est versée, on ne peut plus en débloquer
						msg = "Les subventions {} {} ont déjà été versées, il est impossible d'en débloquer".format(
							str(subvention.vague.type_subvention),
							str(subvention.vague.annee))
						raise forms.ValidationError(msg)
			except KeyError:
				pass

			try:
				if deblocage['montant'] and deblocage['montant'] > subvention.get_rest():
					msg = 'Vous pouvez encore débloquer {} sur {} {}'.format(
						subvention.get_rest(), 
						str(subvention.vague.type_subvention),
						str(subvention.vague.annee))
					raise forms.ValidationError(msg)
			except KeyError:
				pass



class CustomDeblocageSubventionFormSet(BaseInlineFormSet):
	"""sert à définir les critères de validation pour le inlineFormset de modification des déblocages
	de subventions"""

	def clean(self):
		super(CustomDeblocageSubventionFormSet, self).clean()
		if any(self.errors):
			return

		for deblocage in self.cleaned_data:
			if deblocage['montant']:
				if deblocage['montant'] < 0:
					raise forms.ValidationError('Impossible de débloquer des subventions négatives')

				# pour chaque déblocage, il faut prendre en compte le cas ou le montant est None
				# il faut vérifier que le montant n'est pas trop élevé mais aussi que la subvention est encore déblocable
				if deblocage['id'].montant:
					if deblocage['id'].subvention.is_versee and deblocage['id'].montant != deblocage['montant']:
						# si on a tenté de modifier une subvention non déblocable
						msg = "Les subventions {} {} ont déjà été versées, il est impossible de modifier le déblocage".format(
						str(deblocage['id'].subvention.vague.type_subvention),
						str(deblocage['id'].subvention.vague.annee))
						raise forms.ValidationError(msg)

					if deblocage['montant'] > deblocage['id'].subvention.get_rest()+deblocage['id'].montant:
						msg = "Déblocage trop important sur {} {}: vous pouvez débloquer {}".format(
							str(deblocage['id'].subvention.vague.type_subvention), 
							str(deblocage['id'].subvention.vague.annee), 
							deblocage['id'].subvention.get_rest()+deblocage['id'].montant)
						raise forms.ValidationError(msg)
				else:
					if deblocage['id'].subvention.is_versee and deblocage['montant'] > 0:
						# si on a tenté de modifier une subvention non déblocable
						msg = "Les subventions {} {} ont déjà été versées, il est impossible d'en débloquer".format(
						str(deblocage['id'].subvention.vague.type_subvention),
						str(deblocage['id'].subvention.vague.annee))
						raise forms.ValidationError(msg)

					if deblocage['montant'] > deblocage['id'].subvention.get_rest():
						msg = "Déblocage trop important sur {} {}: vous pouvez débloquer {}".format(
							str(deblocage['id'].subvention.vague.type_subvention), 
							str(deblocage['id'].subvention.vague.annee), 
							deblocage['id'].subvention.get_rest())
						raise forms.ValidationError(msg)



		if(self.data['credit'] != '' and float(self.data['credit']) > 0):
			if deblocage['montant']:
				if deblocage['montant'] > 0:
					"""on ne peut pas subventionner une recette"""
					raise forms.ValidationError("Impossible de débloquer des subventions sur une recette")

		somme_deblocages = 0
		for deblocage in self.cleaned_data:
			if deblocage['montant']:
				try:
					somme_deblocages += deblocage['montant']
				except KeyError:
					pass

		if(self.data['debit'] and self.data['debit'] < str(somme_deblocages)):
			print(somme_deblocages)
			raise forms.ValidationError('Impossible de débloquer des subventions supérieures au montant de la dépense')

class PosteDepenseForm(forms.ModelForm):
	"""définit le formulaire pour créer un nouveau poste de dépense"""
	def __init__(self, mandat, *args, **kwargs):
		super(PosteDepenseForm, self).__init__(*args, **kwargs)
		self.mandat = mandat

	class Meta:
		model = PosteDepense
		exclude = ('mandat',)

	def clean(self):
		"""on vérifie que le poste n'est pas dans les postes pour tous dont le mandat est None)"""
		cleaned_data = super(PosteDepenseForm, self).clean()
		print('validating')
		nom = cleaned_data.get('nom')

		if nom in list(PosteDepense.objects.filter(Q(mandat=None) | Q(mandat=self.mandat)).values_list('nom', flat=True)):
			msg = 'Ce nom existe déjà ou est réservé'
			self.add_error('nom', msg)




class SearchLigneForm(forms.Form):
	date_debut = forms.DateField(required=False, label='Après')
	date_fin = forms.DateField(required=False, label='Avant')
	binet = forms.CharField(required=False)
	promotion = forms.ModelChoiceField(queryset=Promotion.objects.all(), required=False)
	poste = forms.ModelChoiceField(queryset=PosteDepense.objects.filter(mandat=None), required=False)
	montant_haut = forms.FloatField(required=False, label='Montant haut')
	montant_bas = forms.FloatField(required=False, label='Montant bas')
	include_locked = forms.BooleanField(initial=False, required=False, label='Inclure les opérations verrouillées')
