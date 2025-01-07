from django.urls import path, include
from django.views.generic import TemplateView

from .views import UserSignUpView, UserLoginView, UserLogoutView, UserDeleteView, verification_view, \
    send_verification_code, password_reset_email, password_reset_verification, PasswordResetView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signup/verification/<int:user_id>/<str:action>/', verification_view, name='verification'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('passwordreset/email/', password_reset_email, name='password_reset_email'),
    path('passwordreset/verification/<int:user_id>/<str:action>/', password_reset_verification, name='password_reset_verification'),
    path('passwordreset/<int:user_id>/', PasswordResetView.as_view(), name='password_reset'),
    path('logout/confirm/', TemplateView.as_view(template_name='accounts/logout-confirm.html'), name='logout_confirm'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('delete/account/<int:pk>/', UserDeleteView.as_view(), name='delete_account'),
    path('delete/warning/', TemplateView.as_view(template_name='accounts/delete-warning.html'), name='delete_warning'),
    path('send_verification_code/<int:user_id>/<str:action>/', send_verification_code, name='send_verification_code'),
]
