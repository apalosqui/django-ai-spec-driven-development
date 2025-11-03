from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, TemplateView

from .forms import ProfileForm, OnboardingForm, FixedExpenseItemForm, VariableAverageForm
from accounts.models import Account
from planning.models import SalaryRule, VariableBudget
from planning.models import FixedExpense
from django.forms import formset_factory


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


class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/onboarding.html'

    def _fixed_formset(self, *args, **kwargs):
        from django.forms import formset_factory
        kwargs.setdefault('extra', 5)
        FixedFormSet = formset_factory(FixedExpenseItemForm, max_num=10, extra=kwargs.pop('extra'))
        return FixedFormSet(*args, **kwargs, prefix='fx')

    def get(self, request, *args, **kwargs):
        form = OnboardingForm()
        formset = self._fixed_formset()
        for f in formset:
            f.apply_tailwind()
        var_form = VariableAverageForm(prefix='vb')
        return self.render_to_response({'form': form, 'formset': formset, 'var_form': var_form})

    def post(self, request, *args, **kwargs):
        form = OnboardingForm(request.POST)
        from django.forms import formset_factory
        FixedFormSet = formset_factory(FixedExpenseItemForm, max_num=10, extra=0)
        formset = FixedFormSet(request.POST, prefix='fx')
        var_form = VariableAverageForm(request.POST, prefix='vb')
        for f in formset:
            f.apply_tailwind()

        if not (form.is_valid() and formset.is_valid() and var_form.is_valid()):
            return self.render_to_response({'form': form, 'formset': formset, 'var_form': var_form})

        user = request.user
        # 1) Caixa
        cash, _ = Account.objects.get_or_create(user=user, name='Caixa', defaults={'opening_balance': 0, 'kind': getattr(Account, 'KIND_CASH', 'CAIXA')})
        opening = form.cleaned_data['opening_balance_cash']
        cash.opening_balance = opening
        cash.save(update_fields=['opening_balance'])

        # 2) Salário
        SalaryRule.objects.update_or_create(
            user=user,
            defaults={
                'amount': form.cleaned_data['salary_amount'],
                'days': (form.cleaned_data.get('salary_days') or '').strip(),
                'ultimo_dia_util': bool(form.cleaned_data.get('ultimo_dia_util')),
            },
        )

        # 3) Reserva
        reserve_name = (form.cleaned_data.get('reserve_name') or '').strip()
        reserve_initial = form.cleaned_data.get('reserve_initial')
        if reserve_name:
            Account.objects.get_or_create(user=user, name=reserve_name, defaults={'opening_balance': reserve_initial or 0, 'kind': getattr(Account, 'KIND_SAVINGS', 'ECONOMIA')})

        # 4) Variável mensal (passo 2)
        vb = var_form.cleaned_data['variable_budget']
        VariableBudget.objects.update_or_create(user=user, category='Gastos Variáveis', defaults={'monthly_amount': vb, 'active': True})

        # 5) Fixos
        # Conta unificada (sem seleção pelo usuário)
        def unified_account():
            acc, _ = Account.objects.get_or_create(user=user, name='Conta Única', defaults={'opening_balance': 0, 'kind': getattr(Account, 'KIND_CASH', 'CAIXA')})
            return acc
        for f in formset:
            cd = f.cleaned_data
            if not cd:
                continue
            name = (cd.get('name') or '').strip()
            amount = cd.get('amount')
            due_day = cd.get('due_day')
            if not name or not amount or not due_day:
                continue
            paying_acc = unified_account()
            FixedExpense.objects.create(
                user=user,
                name=name,
                amount=amount,
                due_day=due_day,
                periodicity=cd.get('periodicity') or 'MENSAL',
                pay_early_business_day=bool(cd.get('pay_early_business_day')),
                paying_account=paying_acc,
            )

        # Redirect to dashboard with onboarding date filter
        onboarding_date = form.cleaned_data['onboarding_date']
        from django.shortcuts import redirect
        return redirect(reverse_lazy('dashboard') + f"?month={onboarding_date.month}&year={onboarding_date.year}&onboarding={onboarding_date:%Y-%m-%d}")
