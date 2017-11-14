from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from django.contrib.auth.models import User
from accounts.models import Promotion, Eleve
from binets.models import Mandat

from .models import ProblemDepart
from .forms import ProblemDepartForm


@permission_required('accounts.see_circuitdepart')
def circuitdepart_home(request):
	"""affiche la page récapitulative par promo"""
	promotions = Promotion.objects.all()

	promotions_data = []
	# on traite pour chaque promotion pour obtenir les totaux
	for promotion in promotions:
		promotion_data = {'promotion': promotion}
		eleves = Eleve.objects.filter(promotion=promotion)
		promotion_data['nb_eleves'] = len(eleves)
		promotion_data['nb_ok'] = len(eleves.filter(all_binets_passed=True).filter(other_problem_circuitdepart=False))
		promotion_data['nb_rest'] = promotion_data['nb_eleves'] - promotion_data['nb_ok']


		promotions_data.append(promotion_data)



	return render(request, 'circuitdepart/circuitdepart_home.html', locals())


@permission_required('accounts.see_circuitdepart')
def recapitulatif_promo(request, promotion):

	# on récupère le paramètre de recherche
	search_arguments = request.GET.get('q', None)

	if search_arguments:
		users = User.objects.filter(eleve__promotion__nom=promotion).filter(Q(eleve__nom__icontains=search_arguments) | Q(eleve__prenom__icontains=search_arguments)).order_by('eleve__nom')
	else:
		users = User.objects.filter(eleve__promotion__nom=promotion).order_by('eleve__nom')


	return render(request, 'circuitdepart/liste_promotion.html', locals())


@permission_required('accounts.see_circuitdepart')
def refresh_all(request):
	"""permet de mettre à jour les gens qui ont encore des binets non passés"""
	users = User.objects.filter(eleve__signed_fiche=False)

	next = request.GET.get('next', '../')

	for user in users:
		if Mandat.objects.filter(Q(president=user) | Q(tresorier=user)).filter(is_active=True).count() == 0:
			try:
				user.eleve.all_binets_passed = True
				user.eleve.save()
			except:
				pass
		else:
			try:
				user.eleve.all_binets_passed = False
				user.eleve.save()
			except:
				pass

	return redirect(next)


@permission_required("accounts.see_circuitdepart")
def fiche_sign_unsign(request, eleve_id):
	next = request.GET.get('next', '../')

	try:
		eleve = Eleve.objects.get(id=eleve_id)
	except:
		return redirect('next')

	eleve.signed_fiche = not(eleve.signed_fiche)
	eleve.save()

	return redirect(next)


@permission_required("circuitdepart.add_problemdepart")
def add_problem(request):
	"""permet d'ajouter un problème à un utilisateur"""

	create_problem_form = ProblemDepartForm(request.POST or None)

	if request.method == 'POST':
		if create_problem_form.is_valid():
			create_problem_form.save()
			user = create_problem_form.cleaned_data['user']
			user.eleve.other_problem_circuitdepart = True
			user.eleve.save()

			return redirect('../' + str(user.eleve.promotion))

	return render(request, 'circuitdepart/add_problem.html', locals())


@permission_required('circuitdepart.add_problemdepart')
def mark_as_resolved(request, id_problem):
	"""permet de marquer comme résolu le problème"""
	next = request.GET.get('next', '../')

	try:
		problem = ProblemDepart.objects.get(id=id_problem)
		print('ok')
	except:
		return redirect(next)

	problem.resolved = not(problem.resolved)
	problem.save()

	if problem.resolved:
		if ProblemDepart.objects.filter(user=problem.user, resolved=False).count() == 0:
			problem.user.eleve.other_problem_circuitdepart = False
	else:
		if not problem.user.eleve.other_problem_circuitdepart:
			problem.user.eleve.other_problem_circuitdepart = True

	problem.user.eleve.save()

	return redirect(next)