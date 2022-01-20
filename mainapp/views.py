from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from mainapp.forms import LoginForm, UserRegistrationForm


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    return render(
        request,
        'index.html'
    )


@login_required
def upload(request):
    return 'test'


# def user_register(request):
#     if request.method == 'POST':
#         user_form = RegisterForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             return render(request, 'account/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаём пользователя, но пока не добавляем в него данные
            new_user = user_form.save(commit=False)
            # Устанавливаем пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя
            new_user.save()
            # Добавляем пользователя в ту или иную группу
            group = Group.objects.get(name=user_form.cleaned_data['group'])
            new_user.groups.add(group)
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})
