from accounts.models import Promotion, Eleve
from binets.models import Binet, TypeBinet, Mandat
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import os
from balisedev import settings


def parse_liste_binets_officielle(imported_binets, sans_echecs=False):
	"""permet de mettre les éléments de la liste officielle des binets suivant le format qui nous intéresse
	Chaque binet possède son indicateur de succès (les infos dans l'excel sont bonnes) et son indicateur de statut
	En effet on n'affiche à l'utilisateur que les modifications effectuées par rapport à la base de données. Cela permet
	de réimporter le fichier de temps en temps et de vérifier que les modifications sont cohérentes
	Le mode sans échec n'est à utiliser que pour le premier import. Il permet d'entrer les anciens binets dont les utilisateurs
	n'ont pas d'identifiants"""
	parsed_binets = []
	for binet in imported_binets:
		parsed_binet = {'errors': [], 'success': True, 'edit': False, 'status': {'binet': None, 'prez': None, 'trez': None}}

		######################################################################
		# INFOS BINET

		try:
			parsed_binet['nom'] = binet['BINET']
		except:
			continue
		parsed_binet['promotion'] = binet['PROMO']
		if type(parsed_binet['promotion']) != int:
			parsed_binet['success'] = False
			parsed_binet['errors'].append("Promotion illisible")
		parsed_binet['description'] = binet['DESCRIPTION']
		try:
			parsed_binet['prez_username'] = binet['Mail Président'].split('@polytechnique.edu')[0]
		except:
			if sans_echecs:
				parsed_binet['prez_username'] = 'Inconnu'
			else:
				parsed_binet['prez_username'] = None
				parsed_binet['success'] = False
				parsed_binet['errors'].append("Pas d'identifiant du président")

		try:
			parsed_binet['trez_username'] = binet['Mail Trésorier'].split('@polytechnique.edu')[0]
		except:
			if sans_echecs:
					parsed_binet['trez_username'] = 'Inconnu'
			else:
				parsed_binet['trez_username'] = None
				parsed_binet['success'] = False
				parsed_binet['errors'].append("Pas d'identifiant du trésorier")


		# type du binet
		parsed_binet['type_binet'] = binet['Chéquier']
		if type(parsed_binet['type_binet']) == float:
			parsed_binet['type_binet'] = 'Sans chéquier'
		elif parsed_binet['type_binet'] == 'x':
			parsed_binet['type_binet'] = 'Avec chéquier'
		elif parsed_binet['type_binet'] == 'h':
			parsed_binet['type_binet'] = 'Compte exté'

		try:
			TypeBinet.objects.get(nom=parsed_binet['type_binet'])
		except ObjectDoesNotExist:
			parsed_binet['success'] = False
			parsed_binet['errors'].append("Type de binet non reconnu")

		##########################################################################
		# nom, prénom du prez
		try:
			nom_prez = binet['PRESIDENT'].split(' ')
			if len(nom_prez) == 2:
				prez_name = nom_prez[0].capitalize().split('-')
				prez_surname = nom_prez[1].capitalize().split('-')
				for k in range(len(prez_name)):
					prez_name[k] = prez_name[k].capitalize()
				for k in range(len(prez_surname)):
					prez_surname[k].capitalize()


				parsed_binet['prez_name'] = ' '.join(prez_name)
				parsed_binet['prez_surname'] = ' '.join(prez_surname)
			else:
				# si les noms sont à plus de 2 items, on utilise le username
				prez_name = parsed_binet['prez_username'].split('.')[1].split('-')
				prez_surname = parsed_binet['prez_username'].split('.')[0].split('-')
				for k in range(len(prez_name)):
					prez_name[k] = prez_name[k].capitalize()
				for k in range(len(prez_surname)):
					prez_surname[k] = prez_surname[k].capitalize()
				parsed_binet['prez_name'] = ' '.join(prez_name)
				parsed_binet['prez_surname'] = ' '.join(prez_surname)
		except:
			parsed_binet['prez_name'] = None
			parsed_binet['prez_surname'] = None
			parsed_binet['success'] = False
			parsed_binet['errors'].append("Nom du président invalide")


		#########################################################################
		# nom, prénom du prez
		try:
			nom_trez = binet['TRESORIER'].split(' ')
			if len(nom_trez) == 2:
				trez_name = nom_trez[0].capitalize().split('-')
				trez_surname = nom_trez[1].capitalize().split('-')
				for k in range(len(trez_name)):
					trez_name[k] = trez_name[k].capitalize()
				for k in range(len(trez_surname)):
					trez_surname[k].capitalize()


				parsed_binet['trez_name'] = ' '.join(trez_name)
				parsed_binet['trez_surname'] = ' '.join(trez_surname)
			else:
				# si les noms sont à plus de 2 items, on utilise le username
				trez_name = parsed_binet['trez_username'].split('.')[1].split('-')
				trez_surname = parsed_binet['trez_username'].split('.')[0].split('-')
				for k in range(len(trez_name)):
					trez_name[k] = trez_name[k].capitalize()
				for k in range(len(trez_surname)):
					trez_surname[k] = trez_surname[k].capitalize()
				parsed_binet['trez_name'] = ' '.join(trez_name)
				parsed_binet['trez_surname'] = ' '.join(trez_surname)
		except:
			parsed_binet['trez_name'] = None
			parsed_binet['trez_surname'] = None
			parsed_binet['success'] = False
			parsed_binet['errors'].append("Nom du trésorier invalide")


		######################################################################
		# on détermine le statut de l'import
		# pour le binet
		if len(Binet.objects.filter(nom=parsed_binet['nom'])) == 0:
			# le binet n'existe pas et il faut le créer
			parsed_binet['edit'] = True
			parsed_binet['status']['binet'] = 'Créer'
		else:
			# pour le mandat
			binet = Binet.objects.get(nom=parsed_binet['nom'])
			promotion, promotion_was_created = Promotion.objects.get_or_create(nom=parsed_binet['promotion'])
			if len(Mandat.objects.filter(binet=binet, promotion=promotion)) == 0:
				parsed_binet['edit'] = True
				parsed_binet['status']['binet'] = 'Mettre à jour'

		# pour le président
		if len(User.objects.filter(username=parsed_binet['prez_username'])) == 0:
			parsed_binet['edit'] = True
			parsed_binet['status']['prez'] = 'Créer'

		# pour le trésorier
		if len(User.objects.filter(username=parsed_binet['trez_username'])) == 0:
			parsed_binet['edit'] = True
			parsed_binet['status']['trez'] = 'Créer'



		if "Pas d'identifiant du président" in parsed_binet['errors'] and not "Pas d'identifiant du trésorier" in parsed_binet['errors']:
			parsed_binet['errors'].append('Cas président non dévoilé')


		parsed_binets.append(parsed_binet)

	return parsed_binets


def create_binet_from_liste_officielle(request, parsed_binets):
	"""permet d'importer la totalité de la liste des binets officielle.
	En revanche tous les binets ne possédant pas les bonnes infos seront ignorés (les vieux)"""
	print('Creating or updating binets and eleves')
	for parsed_binet in parsed_binets:
		if parsed_binet['success'] and parsed_binet['edit']:

			promotion, promotion_was_created = Promotion.objects.get_or_create(nom=parsed_binet['promotion'])

			############################################################################
			# CREATION/UPDATE DES UTILISATEURS
			# on utilise quand même ce test pour le cas ou l'user est plusieurs fois
			# dans la feuille d'import
			try:
				prez_user = User.objects.get(username=parsed_binet['prez_username'])

			except ObjectDoesNotExist:
				prez_user = User.objects.create(
				  	username=parsed_binet['prez_username'],
				  	email=parsed_binet['prez_username']+'@polytechnique.edu')


				keyfile = os.path.join(settings.BASE_DIR, "imports/file_handlers/default.pwd")
				with open(keyfile, "r") as f:
					default_pwd = f.read().strip()
				prez_user.set_password(default_pwd)
				prez_user.save()


				prez_eleve = Eleve.objects.create(
					user=prez_user,
					nom=parsed_binet['prez_name'],
					prenom=parsed_binet['prez_surname'],
					promotion=promotion)
				prez_eleve.save()

			try:
				trez_user = User.objects.get(username=parsed_binet['trez_username'])

			except ObjectDoesNotExist:
				trez_user = User.objects.create(
				  	username=parsed_binet['trez_username'],
				  	email=parsed_binet['trez_username']+'@polytechnique.edu')


				keyfile = os.path.join(settings.BASE_DIR, "imports/file_handlers/default.pwd")
				with open(keyfile, "r") as f:
					default_pwd = f.read().strip()
				trez_user.set_password(default_pwd)
				trez_user.save()


				trez_eleve = Eleve.objects.create(
					user=trez_user,
					nom=parsed_binet['trez_name'],
					prenom=parsed_binet['trez_surname'],
					promotion=promotion)
				trez_eleve.save()

			######################################################################
			# Création/update du binet
			try:
				binet = Binet.objects.get(nom=parsed_binet['nom'])
				binet.description = parsed_binet['description']
				binet.save()
			except ObjectDoesNotExist:
				binet = Binet.objects.create(
					nom=parsed_binet['nom'],
					description=parsed_binet['description'],
					creator=request.user)
				binet.save()

			#######################################################################
			# Création/Update du mandat
			type_binet, type_binet_was_created = TypeBinet.objects.get_or_create(nom=parsed_binet['type_binet'])
			try:
				mandat = Mandat.objects.get(binet=binet, promotion=promotion)
			except ObjectDoesNotExist:
				mandat = Mandat.objects.create(
					binet=binet,
					promotion=promotion,
					type_binet=type_binet,
					president=prez_user,
					tresorier=trez_user,
					creator=request.user)