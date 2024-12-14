from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def parts_list_view(request):
    return render(request, 'parts/list.html')
