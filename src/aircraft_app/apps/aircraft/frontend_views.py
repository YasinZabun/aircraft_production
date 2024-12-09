from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def aircraft_list_view(request):
    return render(request, 'aircraft/list.html')