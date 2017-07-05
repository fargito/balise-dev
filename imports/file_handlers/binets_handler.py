from datetime import datetime

def binets_file_handler(f):
	"""cette fonction est appelée après l'upload d'un fichier
	excel contenant des noms d'élèves"""
	# on commence par enregistrer les données du fichier dans un fichier temporaire
	date = datetime.today()
	filename = 'import_binet_'+str(date.year)+'_'+\
		str(date.month)+'_'+str(date.day)+' '+str(
			date.hour)+'_'+str(date.minute)
	with open('imports/logs/binets_imports/'+filename+'.xls', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


def create_binets(imported_binets):
	"""allows you to create binets from a dict with
	the correct keys"""
	print('Creating or updating eleves:')
	for eleve in imported_eleves:
		# on accepte que les identifiants soient mis en adresse mail polytechnique
		# dans ce cas on effectue le traitement nécessaire
		if '@polytechnique.edu' in eleve['Identifiant']:
			eleve['Identifiant'] = eleve['Identifiant'].split(
				'@polytechnique.edu')[0]
		created_user, user_was_created = User.objects.update_or_create(
			username=eleve['Identifiant'],
			email=eleve['Identifiant']+'@polytechnique.edu')	
		if user_was_created:
			# on ne réinitialise pas les mots de passe si update seulement
			created_user.set_password(eleve['Mot de passe'])
		created_user.save()

		created_eleve, eleve_was_created = Eleve.objects.update_or_create(
			user=created_user, nom=eleve['Nom'],
			prenom=eleve['Prénom'], promotion=Promotion.objects.get(
				nom=eleve['Promotion']))
		created_eleve.save()
		affichage = {True:'Created: ', False:'Updated: '}
		print(affichage[user_was_created],created_user)