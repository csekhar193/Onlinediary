from django.http import HttpResponseForbidden, HttpResponseRedirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf 
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import MyRegistrationForm, MemoryForm, CommentForm, UserForm, ProfileForm
from django.utils import timezone
from Memories.models import Todays_memory, Profile, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def login(request):
	c = {}
	c.update(csrf(request))
	return render(request,'Memories/login.html',c)
	
def auth_view(request):
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
    memories_list = Todays_memory.objects.filter(published_date__lte=timezone.now(), author=request.user).order_by('-published_date')
    paginator = Paginator(memories_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        memories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        memories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        memories = paginator.page(paginator.num_pages)
    return render(request, 'Memories/memories_list.html', {'memories': memories})


def memory_detail(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    return render(request, 'Memories/memory_detail.html', {'memory': memory})


def new_memory(request):
    if request.method == "POST":
        form = MemoryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['text']
            memory = Todays_memory()
            memory.title = title
            memory.text = content
            memory.author = request.user
            memory.save()
            return redirect('memory_detail', pk=memory.pk)
    else:
        form = MemoryForm()
    return render(request, 'Memories/edit_memory.html', {'form': form})

def edit_memory(request, pk):
    if pk:
        memory = get_object_or_404(Todays_memory, pk=pk)
        if  memory.author != request.user:
            return HttpResponseForbidden()
    else:
        memory = Todays_memory(author=request.user)

    if request.method == "POST":
        form = MemoryForm(request.POST, instance=memory)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('text')
            form.title = title
            form.text = content
            form.save()
            return redirect('memory_detail',pk=memory.pk)
    else:
        form = MemoryForm(instance=memory)
    
    return render(request, 'Memories/edit_memory.html', {'form': form})
    
@login_required
def memories_draft_list(request):
    memories_list = Todays_memory.objects.filter(published_date__isnull=True,author=request.user).order_by('-created_date')
    paginator = Paginator(memories_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        memories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        memories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        memories = paginator.page(paginator.num_pages)
    return render(request, 'Memories/memories_draft_list.html', {'memories': memories})

def memory_publish(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    memory.publish()
    return redirect('Memories.views.memory_detail', pk=pk)

def memory_remove(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    memory.delete()
    return redirect('Memories.views.Memories_list')

def public(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    memory.public=True
    memory.save()
    return render(request, 'Memories/memory_detail.html', {'memory': memory})

def private(request, pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    memory.public=False
    memory.save()
    return render(request, 'Memories/memory_detail.html', {'memory': memory})

def public_list(request, username):
    user=User.objects.get(username=username)
    memories_list = Todays_memory.objects.filter(published_date__lte=timezone.now(), author=user.id, public=True).order_by('-published_date')
    paginator = Paginator(memories_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        memories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        memories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        memories = paginator.page(paginator.num_pages)
    return render(request, 'Memories/public.html', {'memories': memories})

def public_detail_view(request,pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    return render(request, 'Memories/publicview.html', {'memory': memory})

def add_comment_to_memory(request,pk):
    memory = get_object_or_404(Todays_memory, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.memory = memory
            comment.todays_memory = memory
            comment.save()
            return redirect('publicview', pk=memory.pk)
    else:
        form = CommentForm()
        return render(request, 'Memories/comment.html', {'form': form})

def profile(request):
    return render(request,'Memories/profile.html',{})

def profile_update(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'Memories/profileupdate.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
def profiles(request):
    if request.method == 'GET':
        user1=request.GET.get('q', None)
        user=User.objects.get(username=user1)
        return render(request,'Memories/profiles.html',{'user': user})

























