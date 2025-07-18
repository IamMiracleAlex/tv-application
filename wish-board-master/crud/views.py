from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Wish

# Create your views here.

def index(request):
    wishes = Wish.objects.all()
    context = {'wishes': wishes}
    return render(request, 'crud/index.html', context)

def create(request):
    wishes = Wish(name=request.POST['name'], wish=request.POST['wish'])
    wishes.save()
    messages.success(request, 'Your wish was added successfully!', extra_tags='alert')
    return redirect('/#wishes')

def edit(request, id):
    wishes = get_object_or_404(Wish, id=id)
    context = {'wishes': wishes}
    return render(request, 'crud/edit.html', context)

def update(request, id):
    wishes = get_object_or_404(Wish, id=id)
    wishes.name = request.POST['name']
    wishes.wish = request.POST['wish']
    wishes.save()
    messages.success(request, 'Your wish was updated successfully!', extra_tags='alert')
    return redirect('/#wishes')

def delete(request, id):
    wishes = get_object_or_404(Wish, id=id)
    wishes.delete()
    messages.success(request, 'Your entry was deleted successfully!', extra_tags='alert')
    return redirect('/#wishes')