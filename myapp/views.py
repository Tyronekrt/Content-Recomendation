
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .models import Content, UserHistory

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import Content, UserHistory
import pickle

# Redirect unauthenticated users to login or authenticated users to dashboard
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

# User Sign-Up View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# User Dashboard with AI Recommendations
@login_required
def dashboard(request):
    user = request.user

    # Load Collaborative Filtering model
    with open('collaborative_model.pkl', 'rb') as model_file:
        algo = pickle.load(model_file)

    # Generate Collaborative Filtering recommendations
    watched_ids = UserHistory.objects.filter(user=user).values_list('content_id', flat=True)
    recommendations_cf = []
    for content_id in Content.objects.exclude(id__in=watched_ids).values_list('id', flat=True):
        predictions = algo.predict(user.id, content_id)
        recommendations_cf.append((content_id, predictions.est))
    recommendations_cf = sorted(recommendations_cf, key=lambda x: x[1], reverse=True)[:5]

    # Fetch recommended Content objects for Collaborative Filtering
    recommended_cf = Content.objects.filter(id__in=[r[0] for r in recommendations_cf])

    # Load Content-Based Filtering model
    with open('content_based_model.pkl', 'rb') as model_file:
        df, similarity_matrix = pickle.load(model_file)

    # Generate Content-Based recommendations
    content_based_recs = []
    for watched_id in watched_ids:
        if watched_id in df['id'].values:
            idx = df[df['id'] == watched_id].index[0]
            similar_items = list(enumerate(similarity_matrix[idx]))
            sorted_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[:5]
            recommended_ids = [df.iloc[i[0]]['id'] for i in sorted_items]
            content_based_recs.extend(Content.objects.filter(id__in=recommended_ids))

    # Combine and de-duplicate recommendations
    recommendations = list(set(recommended_cf) | set(content_based_recs))

    # Fetch user's watched history
    user_history = UserHistory.objects.filter(user=user).order_by('-viewed_at')

    context = {
        'user': user,
        'history': user_history,
        'recommended': recommendations,
    }
    return render(request, 'dashboard.html', context)

# Content Detail View
@login_required
def content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    # Log user interaction
    UserHistory.objects.create(user=request.user, content=content)
    return render(request, 'content_detail.html', {'content': content})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'


def get(request, format=None):
    user = request.user
    recommendations = []

    # Collaborative Filtering logic (similar to the previous code)
    with open('collaborative_model.pkl', 'rb') as model_file:
        algo = pickle.load(model_file)

    watched_ids = UserHistory.objects.filter(user=user).values_list('content_id', flat=True)
    for content_id in Content.objects.exclude(id__in=watched_ids).values_list('id', flat=True):
        predictions = algo.predict(user.id, content_id)
        recommendations.append({'content_id': content_id, 'rating': predictions.est})

    recommendations = sorted(recommendations, key=lambda x: x['rating'], reverse=True)[:5]
    return Response(recommendations, status=status.HTTP_200_OK)


class RecommendationsAPIView(APIView):
    pass