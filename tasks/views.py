from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def tasks_home(request):
	return render(request, 'tasks/tasks_home.html', locals())