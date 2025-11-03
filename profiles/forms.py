from django import forms

from .models import Profile
from datetime import date


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


class OnboardingForm(forms.Form):
    # Obrigatórios
    onboarding_date = forms.DateField(label='Data de início (onboarding)', input_formats=['%Y-%m-%d'], initial=date.today)
    opening_balance_cash = forms.DecimalField(label='Saldo inicial em Caixa (R$)', min_value=0, decimal_places=2, max_digits=12)
    salary_amount = forms.DecimalField(label='Salário mensal (R$)', min_value=0, decimal_places=2, max_digits=12)
    salary_days = forms.CharField(label='Dia(s) de pagamento (ex.: 5,20)', required=False, help_text='Separe por vírgula. Deixe vazio e marque “Último dia útil” se preferir.')
    ultimo_dia_util = forms.BooleanField(label='Último dia útil', required=False)

    # Opcionais
    reserve_name = forms.CharField(label='Nome da reserva (opcional)', required=False)
    reserve_initial = forms.DecimalField(label='Saldo inicial da reserva (R$)', required=False, min_value=0, decimal_places=2, max_digits=12)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes once here; templates render with {{ form.field }}
        text_cls = 'bg-slate-800 border border-slate-700 rounded-md px-3 py-2 w-full text-slate-100'
        for name in ['onboarding_date', 'opening_balance_cash', 'salary_amount', 'salary_days', 'reserve_name', 'reserve_initial']:
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault('class', text_cls)
        self.fields['onboarding_date'].widget.attrs.setdefault('placeholder', 'YYYY-MM-DD')
        self.fields['salary_days'].widget.attrs.setdefault('placeholder', '5,20')


class FixedExpenseItemForm(forms.Form):
    PERIODICITY_CHOICES = (
        ('MENSAL', 'Mensal'),
        ('ANUAL', 'Anual'),
    )
    name = forms.CharField(label='Nome', required=False, max_length=150)
    amount = forms.DecimalField(label='Valor (R$)', required=False, min_value=0, decimal_places=2, max_digits=12)
    due_day = forms.IntegerField(label='Dia de vencimento', required=False, min_value=1, max_value=31)
    periodicity = forms.ChoiceField(label='Periodicidade', choices=PERIODICITY_CHOICES, initial='MENSAL', required=False)
    pay_early_business_day = forms.BooleanField(label='Pagar no dia útil anterior', required=False)

    def apply_tailwind(self):
        text_cls = 'bg-slate-800 border border-slate-700 rounded-md px-3 py-2 w-full text-slate-100'
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Select)):
                field.widget.attrs.setdefault('class', text_cls)

class VariableAverageForm(forms.Form):
    variable_budget = forms.DecimalField(label='Orçamento variável mensal (R$)', min_value=0, decimal_places=2, max_digits=12, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variable_budget'].widget.attrs.setdefault('class', 'bg-slate-800 border border-slate-700 rounded-md px-3 py-2 w-full text-slate-100')
