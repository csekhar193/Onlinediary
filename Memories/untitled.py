url(r'^public/?name=%s/$', views.publicpost, name='publicpost'),



def publicpost(request):
    user1 = request.GET.get('name', None)
    user = User.objects.get(username=user1)
    memories = Todays_memory.objects.filter(published_date__lte=timezone.now(), author=user.id, public=True).order_by('-published_date')
    return render(request, 'Memories/public.html', {'memories': memories})