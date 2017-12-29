from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import VagueSubventions, Subvention

from .helpers import generate_ordering_links
from .helpers import generate_ordering_arguments


@login_required
def subventions_home(request):
	"""affiche des liens vers les subventions triés par année"""
	all_vagues_subventions = VagueSubventions.objects.all()
	# on récupère la liste de toutes les années dans lesquelles ont
	# été accordées des subventions. Comme les vagues de subventions sont
	# ordonnées par (-annee), on a les années en ordre décroissant
	annees = all_vagues_subventions.values('annee').distinct()

	vagues_subventions = []
	for annee in annees:
		vagues_subventions.append((annee['annee'],
			VagueSubventions.objects.filter(
				annee=annee['annee'])))
		
	return render(request, 'subventions/subventions_home.html', locals())


@login_required
def view_vague(request, id_vague):
	"""affiche une vague de subventions"""
	vague = VagueSubventions.objects.get(id=id_vague)
	total_demande, total_accorde, total_debloque, total_rest = vague.get_totals()

	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	
	attributes = ['mandat__binet', 'mandat__promotion', 'mandat__type_binet']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes)

	# on récupère les arguments filtrés
	if arguments:		
		subventions = Subvention.objects.filter(vague=vague).order_by(*arguments)
	else:
		subventions = Subvention.objects.filter(vague=vague)


	# on génère les liens qui serviront à l'ordonnance dans la page
	# si aucun n'a été activé, par défault c'est par nom de binet (index 0)
	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	links_base = '?o='
	ordering_links = list(reversed(generate_ordering_links(ordering, attributes, links_base)))

	if request.user.is_staff:
		public_only = False
	else:
		public_only = True


	return render(request, 'subventions/view_vague.html', locals())


@staff_member_required
def verser_subvention(request, id_subvention):
	"""permet de marquer une subvention comme versée et la verrouiller dans le journal du binet concerné"""

	try:
		subvention = Subvention.objects.get(
			id = id_subvention)
	except KeyError:
		return redirect('../')

	next = request.GET.get('next', subvention.vague.view_self_url())

	subvention.is_versee = not subvention.is_versee
	subvention.save()

	return redirect(next)


@staff_member_required
def verser_subventions_sans_chequier(request, id_vague):
	"""permet de verser/dé-verser toutes les subventions pour les binets sans chéquier"""
	try:
		vague_subventions = VagueSubventions(id=id_vague)
	except KeyError:
		return redirect('../')

	next = request.GET.get('next', vague_subventions.view_self_url())

	subventions = Subvention.objects.filter(vague = vague_subventions, mandat__type_binet__nom='Sans chéquier')

	# pour pouvoir tout dé-verser si on s'est trompé, il faut pouvoir savoir si tout a été versé
	all_versed = True
	for subvention in subventions:
		all_versed &= subvention.is_versee

	for subvention in subventions:
		if all_versed:
			subvention.is_versee = False
		else:
			subvention.is_versee = True
		subvention.save()

	return redirect(next)