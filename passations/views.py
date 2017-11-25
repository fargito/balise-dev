from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from accounts.models import Promotion
from binets.models import Binet, Mandat
from subventions.models import Subvention
from django.db.models import Q

from binets.forms import PassationMandatForm

from subventions.helpers import generate_ordering_arguments, generate_ordering_links



@staff_member_required
def passations_home(request):
	"""affiche les promotions existantes ainsi que les chiffres globaux dessus
	Attention les chiffres affichés concernent uniquement les binets avec ou sans chéquier, pas la Kès ni les comptes extés"""
	promotions = Promotion.objects.all()

	promotions_data = []
	# on traite pour chaque promotion pour obtenir les totaux
	for promotion in promotions:
		promotion_data = {'promotion': promotion}
		mandats = Mandat.objects.filter(promotion=promotion)
		promotion_data['nb_mandats'] = len(mandats)
		promotion_data['nb_passed'] = len(mandats.filter(is_active=False))
		promotion_data['nb_rest'] = promotion_data['nb_mandats'] - promotion_data['nb_passed']
		depenses_promo, recettes_promo, balance_promo = 0, 0, 0
		for mandat in mandats:
			depenses_mandat, recettes_mandat = mandat.get_totals()
			depenses_promo += depenses_mandat
			recettes_promo += recettes_mandat
			balance_promo += recettes_mandat - depenses_mandat
		promotion_data['depenses_promo'] = depenses_promo
		promotion_data['recettes_promo'] = recettes_promo
		promotion_data['balance_promo'] = balance_promo

		promotions_data.append(promotion_data)



	return render(request, 'passations/passations_home.html', locals())


@staff_member_required
def recapitulatif_promo(request, promotion):
	"""displays the promotion's mandats and their statuses"""
	promotion = Promotion.objects.get(nom=promotion)

	# on récupère le paramètre de recherche
	search_arguments = request.GET.get('q', None)

	# on récupère le paramètre d'ordonnance depuis l'url
	ordering = request.GET.get('o', None)
	attributes = ['binet__nom', 'type_binet', 'is_last', 'is_active', 'being_checked']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes, only_one=True)

	# on récupères les binets correspondants à la recherche
	if search_arguments:
		# on transfome la chaine brute en liste pour traiter séparément les mots
		search_arguments_list = search_arguments.split()
		# on construit une liste d'argments Q
		search_list = [Q(binet__nom__icontains=q) for q in search_arguments_list]
		# on concatène ces arguments
		search = search_list.pop()
		for item in search_list:
			search |= item


		if arguments:
			liste_mandats = Mandat.objects.filter(search, promotion=promotion).order_by(*arguments)
		else:
			liste_mandats = Mandat.objects.filter(search, promotion=promotion)
	else:
		if arguments:
			liste_mandats = Mandat.objects.filter(promotion=promotion).order_by(*arguments)
		else:
			liste_mandats = Mandat.objects.filter(promotion=promotion)
	# on ordonne les résultats
	if arguments:
		liste_mandats = liste_mandats.order_by(*arguments)


	# on génère les liens qui serviront à l'ordonnance dans la page
	# si aucun n'a été activé, par défault c'est par nom de binet (index 0)
	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	if search_arguments:
		links_base = 'q=' + search_arguments + '&o='
	else:
		links_base = '?o='
	ordering_links = list(reversed(generate_ordering_links(ordering, attributes, links_base)))



	return render(request, 'passations/recapitulatif_promo.html', locals())


@staff_member_required
def mandat_bilan(request, id_mandat):
	"""view with all the infos on the mandat"""
	next = request.GET.get('next', '../')

	try:
		mandat = Mandat.objects.get(id=id_mandat)
	except KeyError:
		return redirect(next)

	subventions_mandat = Subvention.objects.filter(mandat=mandat)

	passation_mandat_form = PassationMandatForm(request.POST or None, instance=mandat)

	if passation_mandat_form.is_valid():
		mandat = passation_mandat_form.save()

	# on récupère les totaux pour le mandat
	debit_subtotal, credit_subtotal = mandat.get_subtotals()
	debit_total, credit_total = mandat.get_totals()
	balance = credit_total-debit_total
	is_positive = (balance >= 0)

	return render(request, 'passations/mandat_bilan.html', locals())



@staff_member_required
def promotion_bilan(request, promotion):
	"""permet d'afficher de façon plus détaillée le bilan d'une promotion"""
	promotion = Promotion.objects.get(nom=promotion)


	

	return render(request, 'passations/promo_bilan.html', locals())