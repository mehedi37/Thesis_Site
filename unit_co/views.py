from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UnitCoordinator
from project.models import Project
from supervisor.models import Supervisor
from student.models import Student
from thesis_apply.models import ThesisApply
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def pending_projects(request):
    # find all the projects that are not approved by the unit coordinator
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'unit_coordinator':
            projects = Project.objects.select_related('supervisor').order_by('unit_co_approved')
            return render(request, 'pending_projects.html', {'projects': projects})
        else:
            return redirect('project_list')

def unit_coordinators(request):
    # find all the unit coordinators
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            unit_coordinators = UnitCoordinator.objects.all()
            return render(request, 'unit_coordinators.html', {'unit_coordinators': unit_coordinators})
        else:
            return redirect('project_list')
    else:
        return redirect('login')