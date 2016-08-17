from django.http import HttpResponseRedirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf 
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import MyRegistrationForm, MemoryForm
from django.utils import timezone
from .models import Todays_memory
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def login(request):
	c = {}
	c.update(csrf(request))
	return render(request,'Memories/login.html',c)
	
def auth_view(request):
	#if request.method == 'POST':
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user=auth.authenticate(username = username, password = password)
	if user is not None:
	
		auth.login(request,user)
		return redirect('/Home/')
	else:
		return redirect('/accounts/invalid')
	
def invalid(request):
	return render(request,'Memories/invalid.html',{})

def logout_page(request):
    auth.logout(request)
    return redirect('/accounts/login')
	
def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/accounts/register_success')

	args = {}
	args.update(csrf(request))

	args['form'] = MyRegistrationForm()
	return render(request,'Memories/register.html',args)

def register_success(request):
	return render(request,'Memories/register_success.html',{})

@login_required
def Memories_list(request):
    memories = Todays_memory.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'Memories/memories_list.html', {'memories': memories})

def memory_detail(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    return render(request, 'Memories/memory_detail.html', {'memory': memory})

@login_required
def new_memory(request):
    if request.method == "POST":
        form = MemoryForm(request.POST)
        if form.is_valid():
            memory1 = form.save(commit=False)
            memory1.author = request.user
            #memory1.published_date = timezone.now()
            memory1.save()
            return redirect('memory_detail', pk=memory1.pk)
    else:
        form = MemoryForm()
    return render(request, 'Memories/edit_memory.html', {'form': form})

def edit_memory(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    if request.method == "POST":
        form = MemoryForm(request.POST, instance=memory)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.author = request.user
            #memory.published_date = timezone.now()
            memory.save()
            return redirect('memory_detail', pk=memory.pk)
    else:
        form = MemoryForm(instance=memory)
    return render(request, 'Memories/edit_memory.html', {'form': form})

@login_required
def memories_draft_list(request):
    memories = Todays_memory.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'Memories/memories_draft_list.html', {'memories': memories})

def memory_publish(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    memory.publish()
    return redirect('Memories.views.memory_detail', pk=pk)

def memory_remove(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    memory.delete()
    return redirect('Memories.views.Memories_list')












