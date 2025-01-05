from datetime import datetime

from django import forms
from .models import Advertisement, Reaction, User


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'content', 'category']


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['text']


class UserSettingsForm(forms.ModelForm):
    now = datetime.now()
    # birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1950, now.year - 5)))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birthday']


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
        widgets = {
            'avatar': forms.SelectDateWidget()
        }
