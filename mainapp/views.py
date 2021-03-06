import json
import this

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from mainapp.forms import LoginForm, UserRegistrationForm, AristUploadingTrackForm

from django.http import Http404

import pyrebase
import os

from mainapp.models import Track

config = {
    "apiKey": "AIzaSyDcr5w4d3anyiTo7uHHpll0QDlFP_X0ZGA",
    "authDomain": "opengamemusic-d3213.firebaseapp.com",
    "storageBucket": "opengamemusic-d3213.appspot.com",
    "messagingSenderId": "990394749980",
    "appId": "1:990394749980:web:2987d8ec8632fb34c13bd9",
    "databaseURL": "https://opengamemusic-d3213-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def check_user_able_to_see_page(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise Http404

        return wrapper

    return decorator


class TracksListView(generic.ListView):
    model = Track
    template_name = 'index.html'


class TracksDetailView(generic.DetailView):
    model = Track
    template_name = 'track.html'


class TracksSearchView(generic.ListView):
    model = Track
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        track_list = Track.objects.filter(
            Q(name__icontains=query) | Q(published_by__username__icontains=query)
        )
        return track_list


@check_user_able_to_see_page("Artists")
def upload(request):
    if not request.user.is_active:
        return redirect('index')
    if request.method == 'POST':
        form = AristUploadingTrackForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_save = default_storage.save(file.name, file)
            storage.child("tracks/" + request.user.username + '/' + file.name).put("media/" + file.name)
            delete = default_storage.delete(file.name)

            track = form.save(commit=False)

            url = storage.child("tracks/" + request.user.username + '/' + file.name).get_url('5E8D0889-D367-49ED-8C7F'
                                                                                             '-0F3E29A04273')
            track.published_by = request.user
            track.track_url = url
            track.name = form.cleaned_data['title']
            track.save()
            messages.success(request, '???????? ?????? ?????????????? ???????????????? ???? ???????????? ?? ?????????????????????? ???? ??????????')
            return redirect('index')
    else:
        form = AristUploadingTrackForm()
    return render(request, 'upload.html', {'form': form})


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
                    form = LoginForm()
                    return render(request, 'login.html', {'message': '?????? ?????????????? ?????? ??????????????????????????.', 'form': form})
            else:
                form = LoginForm()
                return render(request, 'login.html', {'message': '???????????? ???????????????? ?????????? ?????? ????????????.', 'form': form})
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
            # ?????????????? ????????????????????????, ???? ???????? ???? ?????????????????? ?? ???????? ????????????
            new_user = user_form.save(commit=False)
            # ?????????????????????????? ????????????
            new_user.set_password(user_form.cleaned_data['password'])
            # ?????????????????? ????????????????????????
            new_user.save()
            # ?????????????????? ???????????????????????? ?? ???? ?????? ???????? ????????????
            group = Group.objects.get(name=user_form.cleaned_data['group'])
            new_user.groups.add(group)
            messages.success(request, '???????????? ???? ???????????? ?????????? ?? ??????????????')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@check_user_able_to_see_page("Developers")
def like(request, ids):
    user = request.user
    track = get_object_or_404(Track, id=ids)
    print(track)

    if track.likes.filter(id=user.id).exists():
        track.likes.remove(user)
    else:
        track.likes.add(user)
    return redirect('track-detail', pk=ids)


@check_user_able_to_see_page("Developers")
def views(request, ids2):
    if request.method == "POST":
        user = request.user
        track = get_object_or_404(Track, id=ids2)
        if not track.views.filter(id=user.id).exists():
            track.views.add(user)
    ctx = {'views_count': track.total_views}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
