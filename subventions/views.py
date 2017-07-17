from django.shortcuts import render

from .models import VagueSubventions, Subvention


def subventions_home(request):
	"""affiche des liens vers les subventions triés par année"""
	vagues_subventions = VagueSubventions.objects.all()
	return render(request, 'subventions/subventions_home.html', locals())


def view_vague(request, id_vague):
	"""affiche une vague de subventions"""
	vague = VagueSubventions.objects.get(id=id_vague)
	subventions = Subvention.objects.filter(vague=vague)
	total_demande, total_accorde = vague.get_totals()
	return render(request, 'subventions/view_vague.html', locals())