from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .auth_forms import StudentAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=StudentAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
