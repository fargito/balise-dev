from accounts.models import Promotion, Eleve
from binets.models import Binet, TypeBinet, Mandat
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def create_binets(request,imported_binets):
	"""allows you to create binets from a dict with
	the correct keys"""
	print('Creating or updating binets:')
	request.session['messages'] = []
	for binet in imported_binets:
		# on accepte que les identifiants soient mis en adresse mail polytechnique
		# dans ce cas on effectue le traitement nécessaire
		if '@polytechnique.edu' in binet['Président']:
			binet['Président'] = binet['Président'].split(
			'@polytechnique.edu')[0]
		if '@polytechnique.edu' in binet['Trésorier']:
			binet['Trésorier'] = binet['Trésorier'].split(
			'@polytechnique.edu')[0]
		try:
			# on teste la cohérence du binet: la promotion doit être
			# la même que celle du prez et du trez
			promotion = Promotion.objects.get(nom=binet['Promotion'])
			prez = User.objects.get(username=binet['Président'])
			trez = user=User.objects.get(username=binet['Trésorier'])
			if ((promotion != prez.eleve.promotion) or 
				(prez.eleve.promotion != trez.eleve.promotion) or
				(trez.eleve.promotion != promotion)):
				print("Could not create: {} due to incoherent users promotions".format(binet['Binet']))
				request.session['messages'].append("Impossible de créer: {} incohérence dans les promos".format(binet['Binet']))
			else:
				created_binet, binet_was_created = Binet.objects.update_or_create(
					nom=binet['Binet'], defaults={
					'description': binet['Description'],
					'type_binet': TypeBinet.objects.get(nom=binet['Type']),
					'current_president': prez,
					'current_tresorier': trez,
					'current_promotion': promotion})
				created_binet.save()
				created_mandat, mandat_was_created = Mandat.objects.update_or_create(
					binet=created_binet,
					president=prez,
					tresorier=trez,
					promotion=promotion,
					type_binet=created_binet.type_binet)
				created_mandat.save()
				# si le mandat vient d'être créé on donne
				# aux utilisateurs le droit de modif sur la
				# compta ainsi qu'aux binets précédents
				if mandat_was_created:
					content_type = ContentType.objects.get(app_label='compta', model='Mandat')
					permission = Permission.objects.create(
	    				codename='edit_compta_{0}'.format(created_mandat.id),
	    				name='Modifier la compta de '+str(created_mandat),
	    				content_type=content_type)
					prez.user_permission.add(permission)
					trez.user_permission.add(permission)
					
				affichage = {True:'Created: ', False:'Updated: '}
				print(affichage[binet_was_created],created_binet)
				request.session['messages'].append((affichage[binet_was_created]+str(created_binet)+' ('+str(binet['Promotion'])+')'))	
		except ObjectDoesNotExist:
				print("Could not create: {} due to invalid query: invalid users, promotion or type_binet".format(binet['Binet']))
				request.session['messages'].append("Impossible de créer: {} à cause d'utilisateurs, de promos ou de types de binets non enregistrés dans la base de données".format(binet['Binet']))