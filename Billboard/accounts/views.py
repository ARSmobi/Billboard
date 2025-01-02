from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView

from .forms import SignUpForm, LoginForm, VerificationForm
from .models import VerificationCode
from bboard.models import User


class UserSignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('verification')
    model = User
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        # создание проверочного кода и времени для его удаления
        verification_code = (
            VerificationCode.objects.create(
                user=user,
                delete_at=timezone.now() + timezone.timedelta(hours=1))
        )

        send_mail (
            'Verification Code',
            f'Your verification code is {verification_code.code}',
            'from@example.com',
            [user.email],
        )

        return super().form_valid(form)


def verification_view(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            verification_code = VerificationCode.objects.get(code=code)
            user = verification_code.user
            user.is_active = True
            user.save()
            verification_code.delete()
            return redirect('login')
    else:
        form = VerificationForm()
    return render(request, 'accounts/verification.html', {'form': form})


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            return redirect('verification')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout-confirm.html'
    next_page = 'login'


class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/delete-account.html'
    success_url = reverse_lazy('login')
