from django import forms
from .models import LigneCompta
from subventions.models import DeblocageSubvention



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
	"""définit un formulaire permettant de faire un déblocage de subventions sur une vague"""

	class Meta:
		model = DeblocageSubvention
		fields = ('montant',)

	def clean(self):
		"""on définit la validation pour le paramètre ne dépendant que du champ:
		il doit être positif"""
		cleaned_data = super(DeblocageSubventionForm, self).clean()
		montant = cleaned_data.get('montant')

		if montant < 0:
			msg = 'Ce montant doit être positif'
			self.add_error('montant', msg)