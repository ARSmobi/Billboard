from django.urls import path, include
from django.views.generic import TemplateView

from .views import UserSignUpView, UserLoginView, UserLogoutView, UserDeleteView, verification_view

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signup/verification/', verification_view, name='verification'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/confirm/', TemplateView.as_view(template_name='accounts/logout-confirm.html'), name='logout_confirm'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('delete/account/<int:pk>/', UserDeleteView.as_view(), name='delete_account'),
    path('delete/warning/', TemplateView.as_view(template_name='accounts/delete-warning.html'), name='delete_warning'),
]
