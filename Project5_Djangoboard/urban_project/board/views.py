from django.shortcuts import render, redirect
from board.models import Advertisement
from board.forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})


def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


def advertisement_list_to_edit(request):
    '''Задача №1. Реализовать функционал: Правка объявлений'''
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list_to_edit.html', {'advertisements': advertisements})


def advertisement_detail_edit(request, pk):
    '''Задача №1. Реализовать функционал: Правка объявлений'''
    advertisement = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement.title = form.cleaned_data['title']
            advertisement.content = form.cleaned_data['content']
            advertisement.author = form.cleaned_data['author']
            advertisement.picture = form.files['picture']
            advertisement.save()
            return redirect('board:advertisement_list_to_edit')
    else:
        form = AdvertisementForm()
        form.fields['title'].initial = advertisement.title
        form.fields['content'].initial = advertisement.content
        form.fields['author'].initial = advertisement.author
    return render(request, 'board/advertisement_detail_edit.html', {'form': form})


def advertisement_list_to_delete(request):
    '''Задача №2. Реализовать функционал: Удаление объявлений'''
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list_to_delete.html', {'advertisements': advertisements})


def advertisement_detail_delete(request, pk):
    '''Задача №2. Реализовать функционал: Удаление объявлений'''
    advertisement = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        advertisement.delete()
        return redirect('board:advertisement_list_to_delete')
    return render(request, 'board/advertisement_detail_delete.html', {'advertisement': advertisement})


@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.picture = form.files['picture']
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})
