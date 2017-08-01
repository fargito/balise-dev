from django.shortcuts import render

from .models import VagueSubventions, Subvention

from .helpers import generate_ordering_links
from .helpers import generate_ordering_arguments


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


	return render(request, 'subventions/view_vague.html', locals())