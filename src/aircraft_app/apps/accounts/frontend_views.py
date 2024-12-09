from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return '/dashboard/'

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')
    
