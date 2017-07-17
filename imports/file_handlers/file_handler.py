


def file_handler(f, pathname):
	"""imports a file at pathname"""
	# on commence par enregistrer les données du fichier dans un fichier temporaire
	with open(pathname, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)