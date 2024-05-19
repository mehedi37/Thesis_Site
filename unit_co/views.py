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
    if request.user.is_authenticated:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'unit_coordinator':
            projects = Project.objects.select_related('supervisor').order_by('unit_co_approved')
            return render(request, 'pending_projects.html', {'projects': projects})
        else:
            return redirect('project_list')

def applications(request):
  # get all the thesis_apply objects that are not approved by the unit coordinator
  if request.user.is_authenticated:
    account_type = request.session.get('account_type', 'default_value')
    if account_type == 'unit_coordinator':
      applications = ThesisApply.objects.select_related('applied_student', 'project').order_by('supervisor_approval')
      return render(request, 'applications.html', {'applications': applications})

    elif account_type == 'supervisor':
      try:
        supervisor = Supervisor.objects.get(user=request.user)
        print(f"SupervisorID: {supervisor.user.username}")
        applications = ThesisApply.objects.select_related('applied_student', 'project').filter(project__supervisor__user=supervisor.user).order_by('-supervisor_approval')
        return render(request, 'applications.html', {'applications': applications})
      except ObjectDoesNotExist:
        return HttpResponse('No Supervisor found for this user')

    else:
      return redirect('project_list')

def view_application(request, application_id):
  # view the details of a specific thesis_apply object
  if request.user.is_authenticated:
    account_type = request.session.get('account_type', 'default_value')
    print(f"account_type: {account_type}")
    if account_type == 'unit_coordinator':
      application = ThesisApply.objects.select_related('applied_student', 'project').get(thesis_apply_id=application_id)
      supervisor = Supervisor.objects.get(supervisor_id=application.project.supervisor_id)
      application.supervisor = supervisor
      return render(request, 'view_application.html', {'application': application})

    elif account_type == 'supervisor':
      application = ThesisApply.objects.select_related('applied_student', 'project').get(thesis_apply_id=application_id)
      if application.project.supervisor.user != request.user:
        return HttpResponse('You are not authorized to view this page')
      return render(request, 'view_application.html', {'application': application})

    else:
      return redirect('project_list')
  else:
    return redirect('login')

def delete_application(request, application_id):
  # delete a specific thesis_apply object
  if request.user.is_authenticated:
    account_type = request.session.get('account_type', 'default_value')
    if account_type == 'unit_coordinator':
      application = ThesisApply.objects.get(thesis_apply_id=application_id)
      application.delete()
      return redirect('applications')

    elif account_type == 'supervisor':
      application = ThesisApply.objects.get(thesis_apply_id=application_id)
      if application.project.supervisor.user != request.user:
        return HttpResponse('You are not authorized to delete this application')
      application.delete()
      return redirect('applications_supervisor')

  else:
    return redirect('project_list')

def approve_application(request, application_id):
  # approve a specific thesis_apply object
  if request.user.is_authenticated:
    account_type = request.session.get('account_type', 'default_value')
    if account_type == 'unit_coordinator':
      application = ThesisApply.objects.get(thesis_apply_id=application_id)

      if application.unit_co_checked:
        return HttpResponse('You have already checked this application. Cannot change it again.')

      application.unit_co_checked = True
      application.unit_co_approval = True

      if application.supervisor_approval:
        application.status = 'Approved'
        if not application.project.student.filter(student_id=application.applied_student.id).exists():
              application.project.student.add(application.applied_student.student)

      application.save()
      return redirect('applications')

    elif account_type == 'supervisor':
      application = ThesisApply.objects.get(thesis_apply_id=application_id)
      if application.project.supervisor.user != request.user:
        return HttpResponse('You are not authorized to approve this application')

      if application.supervisor_checked:
        return HttpResponse('You have already checked this application. Cannot change it again.')

      application.supervisor_approval = True
      application.supervisor_checked = True
      if application.unit_co_approval:
        application.status = 'Approved'
        if not application.project.student.filter(student_id=application.applied_student.id).exists():
              application.project.student.add(application.applied_student.student)
      application.save()
      return redirect('applications_supervisor')
    else:
      return redirect('project_list')

def reject_application(request, application_id):
  # reject a specific thesis_apply object
  if request.user.is_authenticated:
    account_type = request.session.get('account_type', 'default_value')
    if account_type == 'unit_coordinator':
      application = ThesisApply.objects.get(thesis_apply_id=application_id)

      if application.unit_co_checked:
        return HttpResponse('You have already checked this application. Cannot change it again.')

      application.unit_co_checked = True
      application.unit_co_approval = False
      if application.supervisor_checked:
        application.status = 'Rejected'
        if application.project.student.exists() and application.project.student.filter(user=application.applied_student.student.user).exists():
              application.project.student.remove(application.applied_student.student)
      application.save()
      return redirect('applications')

    elif account_type == 'supervisor':
      application = ThesisApply.objects.get(thesis_apply_id=application_id)
      if application.project.supervisor.user != request.user:
        return HttpResponse('You are not authorized to reject this application')

      if application.supervisor_checked:
        return HttpResponse('You have already checked this application. Cannot change it again.')

      application.supervisor_approval = False
      application.supervisor_checked = True
      if application.unit_co_checked:
        application.status = 'Rejected'
        if application.project.student.exists() and application.project.student.filter(user=application.applied_student.student.user).exists():
              application.project.student.remove(application.applied_student.student)
      application.save()
      return redirect('applications_supervisor')

    else:
      return redirect('project_list')