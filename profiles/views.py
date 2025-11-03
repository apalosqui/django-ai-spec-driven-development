from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView

from .forms import ProfileForm, OnboardingForm
from accounts.models import Account
from planning.models import SalaryRule, VariableBudget


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'profiles/form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profiles:detail')
    success_message = 'Perfil atualizado com sucesso.'

    def get_object(self, queryset=None):
        return self.request.user.profile


class OnboardingView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'profiles/onboarding.html'
    form_class = OnboardingForm
    success_url = reverse_lazy('dashboard')
    success_message = 'Onboarding concluído com sucesso.'

    def form_valid(self, form):
        user = self.request.user
        # 1) Garantir conta Caixa
        cash, _ = Account.objects.get_or_create(user=user, name='Caixa', defaults={'opening_balance': 0, 'kind': getattr(Account, 'KIND_CASH', 'CAIXA')})
        opening = form.cleaned_data['opening_balance_cash']
        if opening is not None:
            cash.opening_balance = opening
            cash.save(update_fields=['opening_balance'])

        # 2) Salário (regra)
        amount = form.cleaned_data['salary_amount']
        days = (form.cleaned_data.get('salary_days') or '').strip()
        ultimo = bool(form.cleaned_data.get('ultimo_dia_util'))
        SalaryRule.objects.update_or_create(
            user=user,
            defaults={
                'amount': amount,
                'days': days,
                'ultimo_dia_util': ultimo,
            },
        )

        # 3) Variável (opcional)
        vb = form.cleaned_data.get('variable_budget')
        if vb is not None and vb != '':
            VariableBudget.objects.update_or_create(user=user, category='Gastos Variáveis', defaults={'monthly_amount': vb, 'active': True})

        # 4) Reserva (opcional)
        reserve_name = (form.cleaned_data.get('reserve_name') or '').strip()
        reserve_initial = form.cleaned_data.get('reserve_initial')
        if reserve_name:
            Account.objects.get_or_create(user=user, name=reserve_name, defaults={'opening_balance': reserve_initial or 0, 'kind': getattr(Account, 'KIND_SAVINGS', 'ECONOMIA')})

        # 5) Redirecionar para o dashboard já sugerindo a data de onboarding
        onboarding_date = form.cleaned_data['onboarding_date']
        self.success_url = reverse_lazy('dashboard') + f"?month={onboarding_date.month}&year={onboarding_date.year}&onboarding={onboarding_date:%Y-%m-%d}"
        return super().form_valid(form)
