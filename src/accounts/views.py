from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('/accounts/login')
    else:
        form = SignupForm()

    template_name = 'registration/register.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)