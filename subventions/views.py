from django.shortcuts import render

from .models import VagueSubventions, Subvention


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
	subventions = Subvention.objects.filter(vague=vague)
	total_demande, total_accorde, total_debloque, total_rest = vague.get_totals()
	return render(request, 'subventions/view_vague.html', locals())