from django.http import HttpResponse
from django.shortcuts import render, redirect
from project.models import Project
from datetime import datetime
from thesis_apply.models import ThesisApply
from student.models import Student
from unit_co.models import UnitCoordinator

# Create your views here.

def my_projects(request):
    if request.user.is_authenticated:
        account_type = request.session.get('account_type', 'default_value')
        print(f"account_type: {account_type}")
        if account_type == 'supervisor':
            supervisor = request.user.supervisor
            projects = Project.objects.filter(supervisor=supervisor)
            return render(request, 'my_projects.html', {'projects': projects})
        else:
            return redirect('project_list')
    else:
        return redirect('login')

def create_project(request):
    if request.user.is_authenticated:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            if request.method == "POST":
                supervisor = request.user.supervisor
                project = Project()
                project.name = request.POST.get('project_name')
                project.project_detail = request.POST.get('project_detail')

                start_date_str = request.POST.get('start_date')
                end_date_str = request.POST.get('end_date')

                try:
                    project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    if end_date_str:
                        project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    else:
                        project.end_date = None
                except ValueError:
                    return HttpResponse('Invalid date format. It must be in YYYY-MM-DD format.', status=400)

                project.max_students = request.POST.get('max_students')
                project.supervisor = supervisor
                # project.unit_coordinator = UnitCoordinator.objects.get(co_ord_id=1)
                project.save()
                return redirect('my_projects')
            else:
                project = Project()
                return render(request, 'project_details.html',{
                    'project': project,
                })
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return redirect('login')

def edit_project(request, project_id):
    if request.user.is_authenticated:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor' or account_type == 'unit_coordinator':
            project = Project.objects.get(project_id=project_id)
            if (account_type == 'supervisor'):
                supervisor = request.user.supervisor
                project = Project.objects.get(project_id=project_id, supervisor=supervisor)
                if project is None:
                    return HttpResponse('Unauthorized', status=401)

            if request.method == "POST":
                project.name = request.POST.get('project_name')
                project.project_detail = request.POST.get('project_detail')

                start_date_str = request.POST.get('start_date')
                end_date_str = request.POST.get('end_date')

                try:
                    project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    if end_date_str:
                        project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    else:
                        project.end_date = None
                except ValueError:
                    return HttpResponse('Invalid date format. It must be in YYYY-MM-DD format.', status=400)

                project.max_students = request.POST.get('max_students')

                # if teacher edits the project, the unit coordinator approval is reset
                project.unit_co_approved = False
                if account_type == 'unit_coordinator':
                    project.unit_co_approved = 'coordinator_approved' in request.POST

                project.save()

                if account_type == 'unit_coordinator':
                    return redirect('pending_projects')
                return redirect('my_projects')
            else:
                return render(request, 'project_details.html', {'project': project})
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return redirect('login')

def delete_project(request, project_id):
    if request.user.is_authenticated:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            supervisor = request.user.supervisor
            project = Project.objects.get(project_id=project_id, supervisor=supervisor)
            project.delete()
            return redirect('my_projects')

        elif account_type == 'unit_coordinator':
            project = Project.objects.get(project_id=project_id)
            project.delete()
            if account_type == 'unit_coordinator':
                return redirect('pending_projects')
            return redirect('my_projects')
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return redirect('login')