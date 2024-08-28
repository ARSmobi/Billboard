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
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birthday']
        widgets = {
            'birthday': forms.SelectDateWidget()
        }


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
        widgets = {
            'avatar': forms.SelectDateWidget()
        }