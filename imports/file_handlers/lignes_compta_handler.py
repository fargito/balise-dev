from compta.models import LigneCompta



def create_lignes_compta(request, imported_lignes, mandat):
	"""creates compta lines. takes a dict of the values to be put in the line"""
	print('Creating compta lines')
	request.session['messages'] = []
	for ligne in imported_lignes:

		# on commence par supprimer les NaN générés par pandas et les
		# remplacer par des None

		if not ligne['Débit'] > 0:
			ligne['Débit'] = None
		if not ligne['Crédit'] > 0:
			ligne['Crédit'] = None

		created_ligne = LigneCompta.objects.create(
			mandat=mandat,
			date=ligne['Date'],
			auteur=request.user,
			modificateur=request.user,
			description=ligne['Description'],
			debit=ligne['Débit'],
			credit=ligne['Crédit'])
		created_ligne.save()
		request.session['messages'].append('ok')
		print('created a line')