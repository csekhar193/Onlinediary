if request.POST and form.is_valid():
        form = MemoryForm(request.POST, instance=memory)
        form.save()
        return redirect('memory_detail')
    else:
        form = MemoryForm(request.POST, instance=memory)

    return render(request, 'Memories/edit_memory.html', {'form': form})