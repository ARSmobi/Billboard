from django import forms
from .models import Advertisement, Reaction


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'content', 'category']


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['text']
