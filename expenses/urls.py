from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	path('', TemplateView.as_view(template_name='base.html'), name='home'),
	path('register/', views.register, name = 'register'),
	path('login/', views.login_view, name = 'login'),
	path('logout/', views.logout_view, name = 'logout'),
	path('dashboard/', views.dashboard, name = 'dashboard'),
	path('verification-sent/', views.verification_sent, name='verification_sent'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
	path('dashboard/add-bank/', views.add_bank, name='add_bank'),
]