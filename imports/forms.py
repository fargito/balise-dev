from django import forms

class ImportFileForm(forms.Form):
	"""cette classe sert à récupérer un fichier"""
	excel_file = forms.FileField(label="Importez votre fichier")

	#def clean_excel_file(self):
	#	"""on vérifie bien qu'on a bien un fichier excel"""
	#	print("je check si c'est bien un excel")