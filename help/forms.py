from django import forms
from .models import HelpArticle, HelpParagraph
import os
from django.conf import settings


class HelpArticleForm(forms.ModelForm):
	"""permet de créer un HelpArticle"""

	class Meta:
		model = HelpArticle
		exclude = ('filename', 'is_pdf',)


class HelpParagraphForm(forms.ModelForm):
	"""permet de définir un ParagraphForm"""

	class Meta:
		model = HelpParagraph
		fields = '__all__'


class ImportFileForm(forms.Form):
	"""cette classe sert à récupérer un fichier pdf et à checker que c'est bien un pdf"""
	pdf_file = forms.FileField(label="Importez votre fichier")

	def clean(self):
		cleaned_data = super(ImportFileForm, self).clean()
		pdf_file = cleaned_data['pdf_file']
		if not pdf_file.content_type == 'application/pdf':
			msg = "Vous devez importer un pdf"
			self.add_error("pdf_file", msg)

		# on vérifie qu'on ne va pas écraser un fichier existant
		pathname = settings.BASE_DIR + '/help/guides/'
		files_list = os.listdir(pathname)
		if pdf_file.name in files_list:
			msg = "Un fichier du même nom existe déjà, veuillez renommer votre fichier"
			self.add_error("pdf_file", msg)