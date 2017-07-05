from accounts.models import Promotion, Eleve
from binets.models import Binet, TypeBinet, Mandat
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def binets_file_handler(f, pathname):
	"""cette fonction est appelée après l'upload d'un fichier
	excel contenant des noms d'élèves"""
	# on commence par enregistrer les données du fichier dans un fichier temporaire
	with open(pathname, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


def create_binets(request,imported_binets):
	"""allows you to create binets from a dict with
	the correct keys"""
	print('Creating or updating binets:')
	for binet in imported_binets:
		# on accepte que les identifiants soient mis en adresse mail polytechnique
		# dans ce cas on effectue le traitement nécessaire
		if '@polytechnique.edu' in binet['Président']:
			binet['Président'] = binet['Président'].split(
			'@polytechnique.edu')[0]
		if '@polytechnique.edu' in binet['Trésorier']:
			binet['Trésorier'] = binet['Trésorier'].split(
			'@polytechnique.edu')[0]
		# on teste la cohérence du binet: la promotion doit être
		# la même que celle du prez et du trez
		promotion = Promotion.objects.get(nom=binet['Promotion'])
		promotion_prez = Eleve.objects.get(user=User.objects.get(username=binet['Président'])).promotion
		promotion_trez = Eleve.objects.get(user=User.objects.get(username=binet['Trésorier'])).promotion
		if ((promotion != promotion_prez) or 
			(promotion_prez != promotion_trez) or
			(promotion_trez != promotion)):
			print("Could not create: {} due to incoherent users promotions".format(binet['Binet']))
			request.session['message'].append("Impossible de créer: {} incohérence dans les promos".format(binet['Binet']))
		else:
			try:
				created_binet, binet_was_created = Binet.objects.update_or_create(
					nom=binet['Binet'], defaults={
					'description': binet['Description'],
					'type_binet': TypeBinet.objects.get(nom=binet['Type']),
					'current_president': User.objects.get(username=binet['Président']),
					'current_tresorier': User.objects.get(username=binet['Trésorier']),
					'current_promotion': 	Promotion.objects.get(nom=binet['Promotion'])})
				created_binet.save()
				created_mandat, mandat_was_created = Mandat.objects.update_or_create(
					binet=created_binet,
					president=User.objects.get(username=binet['Président']),
					tresorier=User.objects.get(username=binet['Trésorier']),
					promotion=Promotion.objects.get(nom=binet['Promotion']))
				created_mandat.save()
			except ObjectDoesNotExist:
				print("Could not create: {} due to invalid query: invalid users, promotion or type_binet".format(binet['Binet']))
				request.session['message'].append("Impossible de créer: {} à cause d'utilisateurs, de promos ou de types de binets non enregistrés dans la base de données</li>".format(binet['Binet']))
			else:
				affichage = {True:'Created: ', False:'Updated: '}
				print(affichage[binet_was_created],created_binet)
				request.session['message'].append((affichage[binet_was_created]+str(created_binet)+' ('+str(binet['Promotion'])+')'))