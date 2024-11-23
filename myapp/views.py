from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .models import Content, UserHistory


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def dashboard(request):
    contents = Content.objects.all()
    return render(request, 'dashboard.html', {'contents': contents})

@login_required
def content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    UserHistory.objects.create(user=request.user, content=content)
    return render(request, 'content_detail.html', {'content': content})

class CustomLoginView(LoginView):
    template_name = 'login.html'
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})