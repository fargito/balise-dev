from django import forms

class ImportFileForm(forms.Form):
	"""cette classe sert à récupérer un fichier"""
	excel_file = forms.FileField(label="Importez votre fichier")

	def clean(self):
		"""on vérifie bien qu'on a bien un fichier excel"""
		cleaned_data = super(ImportFileForm, self).clean()
		excel_file = cleaned_data['excel_file']

		# TODO find the acceptable formats
		# if not excel_file.content_type == 'application/pdf':
		# 	msg = "Vous devez importer un excel"
		# 	self.add_error("excel_file", msg)
