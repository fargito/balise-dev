from accounts.models import Eleve, Promotion
from django.contrib.auth.models import User


def create_eleves(request, imported_eleves):
	"""allows you to create binets from a dict with
	the correct keys"""
	print('Creating or updating eleves:')
	request.session['messages'] = []
	for eleve in imported_eleves:
		# on accepte que les identifiants soient mis en adresse mail polytechnique
		# dans ce cas on effectue le traitement nécessaire
		if '@polytechnique.edu' in eleve['Identifiant']:
			eleve['Identifiant'] = eleve['Identifiant'].split(
			'@polytechnique.edu')[0]
		created_user, user_was_created = User.objects.update_or_create(
			username=eleve['Identifiant'], defaults={
			'email': eleve['Identifiant']+'@polytechnique.edu'})	
		if user_was_created or created_user.password == None:
			# on ne réinitialise pas les mots de passe si update seulement
			created_user.set_password(eleve['Mot de passe'])
		created_user.save()

		created_eleve, eleve_was_created = Eleve.objects.update_or_create(
			user=created_user, nom=eleve['Nom'],
			prenom=eleve['Prénom'], promotion=Promotion.objects.get(
				nom=eleve['Promotion']))
		created_eleve.save()
		affichage = {True:'Created: ', False:'Updated: '}
		request.session['messages'].append(affichage[user_was_created]+str(created_user))
		print(affichage[user_was_created],created_user)