from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Project
from django.db.models import Q
from django.utils import timezone
from thesis_apply.models import ThesisApply
from thesis_apply.forms import ThesisApplyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from thesis_apply.functions import handleUploadFile
from django.http import HttpResponse


def project_list(request):
    status = request.GET.get('status')
    # print(f"status: {status}")
    projects = Project.objects.select_related('supervisor').filter(unit_co_approved=True)

    # Get the current date and time
    now = timezone.now()

    # Check if there are any projects
    if projects.exists():
        # Filter the projects based on their end_date
        if (status == 'finished'):
            projects = projects.filter(end_date__lte=now)
        elif (status == 'available'):
            projects = projects.filter(
                Q(end_date__gt=now) | Q(end_date__isnull=True))
    else:
        # If there are no projects, return empty lists
        projects = []

    # for all the project in projects add a status key if the project is available or finished
    for project in projects:
        if project.end_date and project.end_date <= timezone.now().date():
            project.status = 'finished'
        else:
            project.status = 'available'

    return render(request, 'project_list.html', {
        'projects': projects,
    })


@login_required
def project_detail(request, project_id):
    project_get = get_object_or_404(Project, pk=project_id)
    if project_get.unit_co_approved == False:
        return HttpResponse("This project is not published by the unit coordinator.")

    if request.method == 'POST':
        form = ThesisApplyForm(request.POST, request.FILES)
        if form.is_valid():
            terms_accepted = form.cleaned_data.get('terms_accepted', False)
            if not terms_accepted:
                return HttpResponse("You must accept the terms and conditions.")

            handleUploadFile(request.FILES['cv'])
            thesis_apply = form.save(commit=False)
            thesis_apply.project = project_get
            thesis_apply.applied_student = request.user
            thesis_apply.save()
            return redirect('project_detail', project_id=project_id)
    elif request.method == 'GET':
        project = Project.objects.get(pk=project_id)
        if project.unit_co_approved == False:
            return HttpResponse("This project is not published by the unit coordinator.")

        thesis_applied = ThesisApply.objects.filter(
            project=project, applied_student=request.user)
        if thesis_applied.exists():
            thesis_applied = thesis_applied.first()
            print(f"thesis_applied: {thesis_applied}")
        else:
            thesis_applied = None
        if project.end_date and project.end_date <= timezone.now().date():
            project.status = 'finished'
        else:
            project.status = 'available'

        form = ThesisApplyForm()
        return render(request, 'project.html', {
            'project': project,
            'form': form,
            'thesis_applied': thesis_applied,
            'required_members': 3,
        })
