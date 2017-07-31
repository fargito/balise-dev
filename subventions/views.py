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
	total_demande, total_accorde, total_debloque, total_rest = vague.get_totals()

	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	
	attributes = ['mandat__binet', 'mandat__promotion', 'mandat__type_binet']
	if ordering:		
		arguments = []
		# on met tous les paramètres dans une liste pour faire l'ordonnance d'un seul coup (sinon ça
		# fait de la merde)
		for index in ordering.split('.'):
			try:
				if '-' in index:
					arguments.append('-'+attributes[abs(int(index))])
				else:
					arguments.append(attributes[int(index)])
			except:
				pass
		subventions = Subvention.objects.filter(vague=vague).order_by(*arguments)

		# on génère les liens qui serviront à l'ordonnance
		links_base = '?o='

		print(ordering)

		ordering_links = []
		for i in range(len(attributes)):
			if '-'+str(i) in ordering:
				sp = ''.join(''.join(ordering.split('-'+str(i))).split('.'))
				if sp:
					ordering_link = links_base + str(i) + '.'+ sp
				else:
					ordering_link = links_base + str(i)
				ordering_links.append(ordering_link)

			elif str(i) in ordering:
				sp = ''.join(''.join(ordering.split(str(i))).split('.'))
				if sp:
					ordering_link = links_base + '-' + str(i) + '.'+ sp
				else:
					ordering_link = links_base + '-' + str(i)
				ordering_links.append(ordering_link)
			else:
				ordering_links.append(
					links_base + str(i) + '.' + ordering)

		print(ordering_links)

	else:
		subventions = Subvention.objects.filter(vague=vague)
		# on génère les liens qui serviront à l'ordonnance dans la page
		# si aucun n'a été activé, par défault c'est par nom de binet
		links_base = '?o='
		ordering_links = [links_base+'-0']
		for i in range(1, len(attributes)):
			ordering_links.append(links_base+str(i))


	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	ordering_links = list(reversed(ordering_links))

	return render(request, 'subventions/view_vague.html', locals())