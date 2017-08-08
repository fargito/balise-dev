from accounts.models import Promotion
from binets.models import Binet, Mandat
from subventions.models import Subvention, TypeSubvention, VagueSubventions
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def create_subventions(request, imported_subventions):
	"""creates the subventions for a given vague"""
	annee = request.session['vague_annee']
	type_subvention = TypeSubvention.objects.get(nom=request.session['vague_type'])
	vague = VagueSubventions.objects.create(
		type_subvention=type_subvention,
		annee=annee)
	request.session['messages'] = ['Created '+str(vague)]
	for subvention in imported_subventions:
		promo, promo_was_created = Promotion.objects.get_or_create(nom=subvention['Promotion'])
		try:
			binet = Binet.objects.get(nom=subvention['Binet'])
		except ObjectDoesNotExist:
			request.session['messages'].append(
				"Could not create '{} ({}): demandé {}€ accordé {}€ postes {}' due to {}".format(
					subvention['Binet'],
					subvention['Promotion'],
					subvention['Demandé'],
					subvention['Accordé'],
					subvention['Postes'],
					'inexistent binet'))
			request.session['messages'].append('Breaking, deleting previous imports...')
			vague.delete()
			request.session['messages'].append('Done')
			return
		else:
			try:
				# pour pouvoir accorder des subventions à des binets qui sont pas encore passés,
				# si le mandat n'existe pas encore, on le crée ?
				mandat = Mandat.objects.get(binet=binet, promotion=promo)
			except ObjectDoesNotExist:
				request.session['messages'].append(
					"Could not create '{} ({}): demandé {}€ accordé {}€ postes {}' due to {}".format(
						subvention['Binet'],
						subvention['Promotion'],
						subvention['Demandé'],
						subvention['Accordé'],
						subvention['Postes'],
						'not yet passed binet'))
				request.session['messages'].append('Breaking, deleting previous imports...')
				vague.delete()
				request.session['messages'].append('Done')
				return
			else:
				try:
					Subvention.objects.create(mandat=mandat,
						accorde=subvention['Accordé'],
						demande=subvention['Demandé'],
						postes=subvention['Postes'],
						vague=vague)
					request.session['messages'].append(
						"Created '{} ({}): demandé {}€ accordé {}€ postes {}'".format(
							subvention['Binet'],
							subvention['Promotion'],
							subvention['Demandé'],
							subvention['Accordé'],
							subvention['Postes']))
				except:
					request.session['messages'].append(
						"Could not create '{} ({}): demandé {}€ accordé {}€ postes {}' due to {}".format(
							subvention['Binet'],
							subvention['Promotion'],
							subvention['Demandé'],
							subvention['Accordé'],
							subvention['Postes'],
							'internal problem'))
					request.session['messages'].append('Breaking, deleting previous imports...')
					vague.delete()
					request.session['messages'].append('Done')
					return
	request.session['messages'].append("Finished importing the subventions")