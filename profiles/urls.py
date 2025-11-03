from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView, OnboardingView


app_name = 'profiles'


urlpatterns = [
    path('', ProfileDetailView.as_view(), name='detail'),
    path('editar/', ProfileUpdateView.as_view(), name='edit'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
]
