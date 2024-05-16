from django.shortcuts import render
from django.utils import timezone
from .models import Project
from django.db.models import Q
from django.utils import timezone


def project_list(request):
    status = request.GET.get('status')
    # print(f"status: {status}")
    projects = Project.objects.select_related('supervisor', 'unit_coordinator')

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
