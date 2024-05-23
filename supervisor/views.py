from django.http import HttpResponse
from django.shortcuts import render, redirect
from project.models import Project
from datetime import datetime
from thesis_apply.models import ThesisApply
from student.models import Student
from unit_co.models import UnitCoordinator
from supervisor.models import Supervisor
from django.core.exceptions import ObjectDoesNotExist
from chat.models import Conversation, Message
from django.db import transaction
from django.shortcuts import redirect
from thesis_apply.models import ThesisApply


# Create your views here.

def my_projects(request):
    if request.user.is_authenticated and not request.user.is_superuser:
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
    if request.user.is_authenticated and not request.user.is_superuser:
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
    if request.user.is_authenticated and not request.user.is_superuser:
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
    if request.user.is_authenticated and not request.user.is_superuser:
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

def applications(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            try:
                supervisor = Supervisor.objects.get(user=request.user)
                applications = ThesisApply.objects.prefetch_related('applied_students', 'project').filter(project__supervisor__user=supervisor.user).order_by('-supervisor_approval')
                return render(request, 'applications.html', {'applications': applications})
            except ObjectDoesNotExist:
                return HttpResponse('No Supervisor found for this user')
        else:
            return redirect('project_list')
    else:
        return redirect('login')

def view_application(request, application_id):
    # view the details of a specific thesis_apply object
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            application = ThesisApply.objects.prefetch_related('applied_students', 'project').get(thesis_apply_id=application_id)
            if application.project.supervisor.user != request.user:
                return HttpResponse('You are not authorized to view this page')
            return render(request, 'view_application.html', {'application': application})
        else:
            return redirect('project_list')
    else:
        return redirect('login')

def delete_application(request, application_id):
    # delete a specific thesis_apply object
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            application = ThesisApply.objects.get(thesis_apply_id=application_id)
            if application.project.supervisor.user != request.user:
                return HttpResponse('You are not authorized to delete this application')
            application.delete()
            return redirect('applications')
        else:
            return redirect('project_list')
    else:
        return redirect('login')

@transaction.atomic
def approve_application(request, application_id):
    # approve a specific thesis_apply object
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            application = ThesisApply.objects.get(thesis_apply_id=application_id)
            if application.project.supervisor.user != request.user:
                return HttpResponse('You are not authorized to approve this application')
            if application.supervisor_checked:
                return HttpResponse('You have already checked this application. Cannot change it again.')

            application.supervisor_approval = True
            application.supervisor_checked = True
            application.status = 'Approved'
            if application.project.student.exists() and application.project.student.filter(user=application.applied_student.student.user).exists():
                application.project.student.add(application.applied_student.student)
            application.save()

            supervisor = Supervisor.objects.get(user=request.user)
            # Create a new conversation for each group of students that applied
            group = application.applied_students.first().user.groups.first()
            conversation = Conversation.objects.create(
                conversation_title=f"{supervisor.user.username} - {group.name}",
                supervisor=supervisor,
                group=group,
            )
            # Create a new message
            Message.objects.create(
                conversation=conversation,
                user=request.user,
                message=f"Group: \"{group.name}\", Your application has been approved !",
            )

            return redirect('applications')
        else:
            return redirect('project_list')
    else:
        return redirect('login')


def reject_application(request, application_id):
    # reject a specific thesis_apply object
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            application = ThesisApply.objects.get(thesis_apply_id=application_id)
            if application.project.supervisor.user != request.user:
                return HttpResponse('You are not authorized to reject this application')
            if application.supervisor_checked:
                return HttpResponse('You have already checked this application. Cannot change it again.')
            application.supervisor_approval = False
            application.supervisor_checked = True
            application.status = 'Rejected'
            if application.project.student.exists() and application.project.student.filter(user=application.applied_student.student.user).exists():
                application.project.student.remove(application.applied_student.student)
            application.save()
            return redirect('applications')
        else:
            return redirect('project_list')
    else:
        return redirect('login')


def message_unit_co(request, unit_co_id):
    if request.user.is_authenticated and not request.user.is_superuser:
        account_type = request.session.get('account_type', 'default_value')
        if account_type == 'supervisor':
            supervisor = request.user.supervisor
            unit_co = UnitCoordinator.objects.get(co_ord_id=unit_co_id)
            if unit_co is None:
                return HttpResponse('Unit Coordinator not found', status=404)

            # Check if a conversation with the same unit coordinator and supervisor exists
            conversation = Conversation.objects.filter(supervisor=supervisor, unit_co=unit_co, group=None).first()
            if conversation is None:
                # Create a new conversation
                conversation = Conversation.objects.create(
                    conversation_title=f"{supervisor.user.username} - {unit_co.user.username}",
                    supervisor=supervisor,
                    unit_co=unit_co,
                )
                # Create a new message
                Message.objects.create(
                    conversation=conversation,
                    user=request.user,
                    message="Conversation created!",
                )
            # Redirect to the conversation
            return redirect('conversation', conversation_id=conversation.conversation_id)
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return redirect('login')