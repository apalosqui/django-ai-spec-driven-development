from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


INPUT_CLASS = 'bg-slate-800 border border-slate-700 rounded-md px-3 py-2 w-full text-slate-100'


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'class': INPUT_CLASS}),
        }
        labels = {
            'email': 'E-mail',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('As senhas não conferem.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Username represents AUTH_USER_MODEL.USERNAME_FIELD (email in this app)
        self.fields['username'].label = 'E-mail'
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASS, 'autocomplete': 'email'})
        self.fields['password'].label = 'Senha'
        self.fields['password'].widget.attrs.update({'class': INPUT_CLASS})
