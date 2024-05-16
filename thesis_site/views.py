from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from student.models import Student
from supervisor.models import Supervisor
from unit_co.models import UnitCoordinator


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

                    # get the name of the account type
                    acType = account_models[account_type].__name__

                    if account_models[account_type].objects.filter(user=user).exists():
                        login(request, user)
                        request.session['account_type'] = account_type
                        return redirect('project_list')
                    else:
                        messages.error(
                            request, f'Invalid {acType} data. Make use the user is a {acType}.')
                else:
                    messages.error(request, 'Invalid account type')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(
                request, 'Invalid form data. Check username and password')
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


def register(request):
    if request.method == 'POST':
        account_type = request.POST['account_type']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        repassword = request.POST['password2']

        if password != repassword:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        print(
            f"account_type: {account_type} username: {username} email: {email} password: {password}")

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            if account_type == 'student':
                student = Student.objects.create(
                    user=user
                )
                student.save()
            elif account_type == 'supervisor':
                supervisor = Supervisor.objects.create(
                    user=user
                )
                supervisor.save()
            elif account_type == 'unit_coordinator':
                unit_coordinator = UnitCoordinator.objects.create(
                    user=user
                )
                unit_coordinator.save()

            messages.success(request, 'You are now registered and can log in')
            return redirect('login')
    else:
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('project_list')
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
