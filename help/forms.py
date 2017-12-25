from django import forms
from .models import HelpArticle

class HelpArticleForm(forms.ModelForm):
	"""permet de créer un HelpArticle"""

	class Meta:
		model = HelpArticle
		exclude = ('filename', 'is_pdf',)


class ImportFileForm(forms.Form):
	"""cette classe sert à récupérer un fichier pdf et à checker que c'est bien un pdf"""
	pdf_file = forms.FileField(label="Importez votre fichier")

	def clean(self):
		cleaned_data = super(ImportFileForm, self).clean()
		pdf_file = cleaned_data['pdf_file']
		if not pdf_file.content_type == 'application/pdf':
			msg = "Vous devez importer un pdf"
			self.add_error("pdf_file", msg)