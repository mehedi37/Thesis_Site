from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from student.models import Student, Group
from supervisor.models import Supervisor
from unit_co.models import UnitCoordinator
from django.contrib import messages
from thesis_apply.functions import handleUploadFile
from django.db import transaction

from django.contrib.auth.hashers import make_password




def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and not user.is_superuser:
                account_type = request.POST.get('account_type')
                account_models = {
                    'student': Student,
                    'supervisor': Supervisor,
                    'unit_coordinator': UnitCoordinator,
                }

                if account_type in account_models:
                    acType = account_models[account_type].__name__

                    if account_type == 'student':
                        if Student.objects.filter(user=user).exists():
                            login(request, user)
                            request.session['account_type'] = account_type
                            return redirect('project_list')
                        else:
                            messages.error(request, f'Invalid {acType} data. Make sure the user is a {acType}.')
                    elif account_models[account_type].objects.filter(user=user).exists():
                        login(request, user)
                        request.session['account_type'] = account_type
                        return redirect('project_list')
                    else:
                        messages.error(request, f'Invalid {acType} data. Make sure the user is a {acType}.')
                else:
                    messages.error(request, 'Invalid account type')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form data. Check username and password')
    else:
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('project_list')
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')
    return render(request, 'logout.html')


def register_admin(request):
    if request.method == 'POST':
        account_type = request.POST['account_type']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        repassword = request.POST['password2']

        if password != repassword:
            messages.error(request, 'Passwords do not match')
            return redirect('register_admin')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register_admin')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)

            supervisor_group, created = Group.objects.get_or_create(name='supervisor')
            unit_coordinator_group, created = Group.objects.get_or_create(name='unit_coordinator')

            if account_type == 'supervisor':
                supervisor = Supervisor.objects.create(user=user)
                supervisor.save()
                supervisor_group.user_set.add(user)
            elif account_type == 'unit_coordinator':
                unit_coordinator = UnitCoordinator.objects.create(user=user)
                unit_coordinator.save()
                unit_coordinator_group.user_set.add(user)

            messages.success(request, 'You are now registered and can log in')
            return redirect('login')
    else:
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('project_list')
        form = UserCreationForm()
    return render(request, 'register_admin.html', {'form': form})


def register(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']

        try:
            with transaction.atomic():
                # Get or create a group
                group, created = Group.objects.get_or_create(name=group_name)
                if not created:
                    messages.error(request, 'Group name already exists')
                    return redirect('register')

                # Check if any of the usernames already exist
                student_count = len([key for key in request.POST.keys() if key.startswith('username')])
                usernames = [request.POST[f'username{i}'] for i in range(1, student_count + 1)]
                if User.objects.filter(username__in=usernames).exists():
                    messages.error(request, 'One or more usernames already exist')
                    return redirect('register')

                # Create a user and a student profile for each student in the group
                students = []
                for i in range(1, student_count + 1):
                    username = usernames[i - 1]
                    password = request.POST[f'password{i}']

                    user = User.objects.create_user(
                        username=username,
                        password=password
                    )
                    user.groups.add(group)

                    # Handle the uploaded CV
                    cv = request.FILES.get(f'cv{i}')
                    if cv:
                        cv_url = handleUploadFile(cv)
                        # Create a new student profile
                        students.append(
                            Student(
                                user=user,
                                group=group,
                                cv=cv_url,
                                address=request.POST.get(f'address{i}', '')
                            )
                        )

                Student.objects.bulk_create(students)

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('register')

        messages.success(request, 'You are now registered and can log in')
        return redirect('login')

    else:
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('project_list')
        return render(request, 'register.html')

