

def eleves_file_handler(f):
	"""cette fonction est appelée après l'upload d'un fichier
	excel contenant des noms d'élèves"""
	# on commence par enregistrer les données du fichier dans un fichier temporaire
	with open('imports/logs/eleves_imports/names.xls', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)