from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

@login_required(login_url='accounts/login')
def home(request):
    template_name = 'home/home.html'
    context = {
        'title': "Home",
    }
    return render(request, template_name, context)

