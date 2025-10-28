from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name']
        labels = {
            'full_name': 'Nome completo',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'autocomplete': 'name'}),
        }

