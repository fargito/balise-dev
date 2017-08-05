from compta.models import LigneCompta, PosteDepense
import pandas
import datetime


def validate_import_lignes(request, imported_lignes, mandat):
	"""permet de valider l'import de lignes compta et de sortir à l'utilisateur quelles sont les erreurs"""
	# permet de suivre la validité de l'import
	parsed_imports = []
	is_valid = True
	for imported_ligne in imported_lignes:
		parsed_import = {'errors':[]}
		# on commence par vérifier la présence des titres des colonnes qui se retrouvent donc comme key des dicts
		# on est un peu laxiste sur les accents et les majuscules


		########################################################
		# Débit

		try:
			parsed_import['debit'] = imported_ligne['Débit']
		except:
			try:
				parsed_import['debit'] = imported_ligne['Debit']
			except:
				try:
					parsed_import['debit'] = imported_ligne['débit']
				except:
					try:
						parsed_import['debit'] = imported_ligne['debit']
					except:
						parsed_import['errors'].append('Pas de débit trouvé')
						is_valid = False
		# on remplace les valeurs vides par None
		try:
			if not float(parsed_import['debit']) > 0:
				parsed_import['debit'] = None
			else:
				parsed_import['debit'] = float(parsed_import['debit'])
		except:
			parsed_import['errors'].append('Mauvais format de débit')
			is_valid = False

		###########################################################
		# Crédit

		try:
			parsed_import['credit'] = imported_ligne['Crédit']
		except:
			try:
				parsed_import['credit'] = imported_ligne['Credit']
			except:
				try:
					parsed_import['credit'] = imported_ligne['crédit']
				except:
					try:
						parsed_import['credit'] = imported_ligne['credit']
					except:
						parsed_import['errors'].append('Pas de crédit trouvé')
						is_valid = False
		# on remplace les valeurs vides par None
		try:
			if not float(parsed_import['credit']) > 0:
				parsed_import['credit'] = None
			else:
				parsed_import['credit'] = float(parsed_import['credit'])
		except:
			parsed_import['errors'].append('Mauvais format de crédit')
			is_valid = False

		#######################################################
		# Date


		try:
			parsed_import['date'] = imported_ligne['Date']
		except:
			try:
				parsed_import['date'] = imported_ligne['date']
			except:
				parsed_import['errors'].append('')
				is_valid = False


		try:
			parsed_import['date'] = parsed_import['date'].to_datetime()
		except:
			if not type(parsed_import['date']) == datetime.datetime:
				is_valid = False
				parsed_import['errors'].append('Mauvais format de date')

		########################################################
		# Description

		try:
			parsed_import['description'] = imported_ligne['Description']
		except:
			try:
				parsed_import['description'] = imported_ligne['description']
			except:
				parsed_import['errors'].append('Pas de description trouvée')
				is_valid = False

		# on n'accepte pas les valeurs vides
		try:
			if not float(parsed_import['description']) > 0:
				is_valid = False
				parsed_import['errors'].append('Description vide')
		except:
			pass

		########################################################
		# Poste de dépenses

		try:
			parsed_import['poste'] = imported_ligne['Poste']
		except:
			try:
				parsed_import['poste'] = imported_ligne['poste']
			except:
				parsed_import['poste'] = None
		# on remplace les valeurs vides par None
		try:
			if not float(parsed_import['poste']) > 0:
				parsed_import['poste'] = None
		except:
			pass

		# pour polymédia on met au bon format
		if (parsed_import['poste'] == 'Polymedia' or parsed_import['poste'] == 'polymedia' or parsed_import['poste'] == 'polymédia' or parsed_import['poste'] == 'CPM' or parsed_import['poste'] == 'cpm'):
			parsed_import['poste'] = 'Polymédia'

		# tests de la cohérence de la ligne

		if parsed_import['debit'] and parsed_import['credit']:
			is_valid = False
			parsed_import['errors'].append('Une ligne ne peut pas être à la fois débit et crédit')


		parsed_imports.append(parsed_import)

	return is_valid, parsed_imports


def create_lignes_compta(request, imported_lignes, mandat):
	"""creates compta lines. takes a dict of the values to be put in the line"""
	print('Creating compta lines')
	request.session['messages'] = []
	for ligne in imported_lignes:

		# on commence par récupérer le poste de dépense
		poste = ligne['poste']

		# si le poste est attribué à tous, on ne le recrée pas pour ce mandat
		if poste:
			if poste in list(PosteDepense.objects.filter(mandat=None).values_list('nom', flat=True)):
				poste = PosteDepense.objects.get(mandat=None, nom=poste)
			else:
				poste, is_created = PosteDepense.objects.get_or_create(mandat=mandat, nom=poste)

		created_ligne = LigneCompta.objects.create(
			mandat=mandat,
			date=ligne['date'],
			auteur=request.user,
			modificateur=request.user,
			description=ligne['description'],
			poste_depense=poste,
			debit=ligne['debit'],
			credit=ligne['credit'])
		created_ligne.save()
		request.session['messages'].append('ok')