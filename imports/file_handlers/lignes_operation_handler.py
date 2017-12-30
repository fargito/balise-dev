from compta.models import LigneCompta, PosteDepense, HiddenOperation
from binets.models import Mandat
import pandas
import datetime

from django.core.exceptions import ObjectDoesNotExist


def validate_import_lignes_operation(request, imported_lignes, operation):
	"""permet de valider l'import de lignes compta sur une operation"""
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
				parsed_import['date'] = ''

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

		##########################################################
		# Référence

		try:
			parsed_import['reference'] = imported_ligne['Référence']
		except:
			try:
				parsed_import['reference'] = imported_ligne['Reference']
			except:
				try:
					parsed_import['reference'] = imported_ligne['référence']
				except:
					try:
						parsed_import['reference'] = imported_ligne['reference']
					except:
						parsed_import['reference'] = None

		# on remplace les valeurs vides par None
		try:
			if not float(parsed_import['reference']) > 0:
				parsed_import['reference'] = None
		except:
			pass


		##########################################################
		# Binet

		try:
			parsed_import['binet'] = imported_ligne['Binet']
		except:
			try:
				parsed_import['binet'] = imported_ligne['binet']
			except:
				parsed_import['binet'] = None

		# on remplace les valeurs vides par None
		try:
			if not float(parsed_import['binet']) > 0:
				parsed_import['binet'] = None
		except:
			pass

		##########################################################
		# Promotion

		try:
			parsed_import['promotion'] = imported_ligne['Promotion']
		except:
			try:
				parsed_import['promotion'] = imported_ligne['promotion']
			except:
				parsed_import['promotion'] = None

		# on remplace les valeurs vides par None
		try:
			if not float(parsed_import['promotion']) > 0:
				parsed_import['promotion'] = None
		except:
			pass

		##############################################################
		# tests de la cohérence de la ligne

		if parsed_import['debit'] and parsed_import['credit']:
			is_valid = False
			parsed_import['errors'].append('Une ligne ne peut pas être à la fois débit et crédit')

		# test de l'existence du mandat

		try:
			mandat = Mandat.objects.get(promotion__nom=parsed_import['promotion'],
										binet__nom=parsed_import['binet'])
		except ObjectDoesNotExist:
			is_valid = False
			parsed_import['errors'].append("Le mandat n'existe pas")


		parsed_imports.append(parsed_import)

	return is_valid, parsed_imports


def create_lignes_compta_operation(request, imported_lignes, operation):
	"""creates compta lines. takes a dict of the values to be put in the line
	Attention toutes les lignes créées sont directement locked"""
	print('Creating compta lines')
	request.session['messages'] = []
	for ligne in imported_lignes:
		# on récupère le mandat
		mandat = Mandat.objects.get(promotion__nom=ligne['promotion'],
									binet__nom=ligne['binet'])

		created_ligne = LigneCompta.objects.create(
			hidden_operation=operation,
			is_locked=True,
			mandat=mandat,
			date=ligne['date'],
			reference=ligne['reference'],
			auteur=request.user,
			modificateur=request.user,
			description=ligne['description'],
			debit=ligne['debit'],
			credit=ligne['credit'])
		created_ligne.save()
		request.session['messages'].append('ok')