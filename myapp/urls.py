from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home_redirect, name='home'),
path('', views.CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),

    path('accounts/logout/', views.CustomLoginView.as_view(), name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),  # New signup view
]
