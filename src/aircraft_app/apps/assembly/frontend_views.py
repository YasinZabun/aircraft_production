from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def assemble_view(request):
    # Only assembly team should use this page, but we'll rely on backend logic to restrict functionality
    return render(request, 'assembly/assemble.html')
