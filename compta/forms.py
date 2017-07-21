from django import forms
from .models import LigneCompta
from subventions.models import DeblocageSubvention
from django.forms import BaseFormSet, BaseInlineFormSet



class LigneComptaForm(forms.ModelForm):
	"""this form is used in the compta journal to enter
	a new compta opération"""
	
	class Meta:
		model = LigneCompta
		exclude = ('mandat','auteur','modificateur', 'add_date', 'edit_date')
		required = {'credit': False, 'debit': False}

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
	def clean(self):
		if any(self.errors):
			"""on se fait pas chier à valider le formset si un des formulaires a une erreur"""
			return

		if(self.data['credit'] and float(self.data['credit']) > 0):
			"""on ne peut pas subventionner une recette"""
			raise forms.ValidationError("Impossible de débloquer des subventions sur une recette")

		print(self.cleaned_data)
		somme_deblocages = 0
		for deblocage in self.cleaned_data:
			try:
				if deblocage['montant']:
					somme_deblocages += deblocage['montant']
			except KeyError:
				pass

		if(float(self.data['debit']) < somme_deblocages):
			raise forms.ValidationError('Impossible de débloquer des subventions supérieures au montant de la dépense')



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

				if deblocage['id'].montant and deblocage['montant'] > deblocage['id'].subvention.get_rest()+deblocage['id'].montant:
					msg = "Déblocage trop important sur {} {}: vous pouvez débloquer {}".format(
						str(deblocage['id'].subvention.vague.type_subvention), 
						str(deblocage['id'].subvention.vague.annee), 
						deblocage['id'].subvention.get_rest()+deblocage['id'].montant)
					raise forms.ValidationError(msg)
				elif deblocage['montant'] > deblocage['id'].subvention.get_rest():
					msg = "Déblocage trop important sur {} {}: vous pouvez débloquer {}".format(
						str(deblocage['id'].subvention.vague.type_subvention), 
						str(deblocage['id'].subvention.vague.annee), 
						deblocage['id'].subvention.get_rest())
					raise forms.ValidationError(msg)



		if(self.data['credit'] != '' and float(self.data['credit']) > 0):
			"""on ne peut pas subventionner une recette"""
			raise forms.ValidationError("Impossible de débloquer des subventions sur une recette")

		somme_deblocages = 0
		for deblocage in self.cleaned_data:
			if deblocage['montant']:
				try:
					somme_deblocages += deblocage['montant']
				except KeyError:
					pass

		if(self.data['debit'] and float(self.data['debit']) < somme_deblocages):
			print(somme_deblocages)
			raise forms.ValidationError('Impossible de débloquer des subventions supérieures au montant de la dépense')