from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormView

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


class OnboardingView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'profiles/onboarding.html'
    form_class = OnboardingForm
    success_url = reverse_lazy('profiles:onboarding-fixed')
    success_message = 'Dados iniciais salvos. Agora cadastre seus fixos.'

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
        # Guardar para o próximo passo
        self.request.session['onboarding_date'] = onboarding_date.strftime('%Y-%m-%d')
        return super().form_valid(form)


class OnboardingFixedView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/onboarding_fixed.html'

    def get(self, request, *args, **kwargs):
        FixedFormSet = formset_factory(FixedExpenseItemForm, extra=5, max_num=10)
        formset = FixedFormSet(prefix='fx')
        accounts = Account.objects.filter(user=request.user)
        choices = [(str(a.id), a.name) for a in accounts]
        for f in formset:
            f.fields['paying_account'].choices = choices
            f.apply_tailwind()
        var_form = VariableAverageForm(prefix='vb')
        return self.render_to_response({'formset': formset, 'var_form': var_form})

    def post(self, request, *args, **kwargs):
        FixedFormSet = formset_factory(FixedExpenseItemForm, extra=0)
        formset = FixedFormSet(request.POST, prefix='fx')
        var_form = VariableAverageForm(request.POST, prefix='vb')
        accounts = Account.objects.filter(user=request.user)
        choices = [(str(a.id), a.name) for a in accounts]
        for f in formset:
            f.fields['paying_account'].choices = choices
            f.apply_tailwind()
        if formset.is_valid() and var_form.is_valid():
            # Salvar variável mensal
            vb = var_form.cleaned_data['variable_budget']
            VariableBudget.objects.update_or_create(user=request.user, category='Gastos Variáveis', defaults={'monthly_amount': vb, 'active': True})
            # Salvar fixos válidos
            for f in formset:
                cd = f.cleaned_data
                if not cd:
                    continue
                name = (cd.get('name') or '').strip()
                amount = cd.get('amount')
                due_day = cd.get('due_day')
                if not name or not amount or not due_day:
                    continue
                periodicity = cd.get('periodicity') or 'MENSAL'
                pay_early = bool(cd.get('pay_early_business_day'))
                acc_id = cd.get('paying_account')
                try:
                    paying_acc = accounts.get(id=int(acc_id)) if acc_id else accounts.first()
                except Exception:
                    paying_acc = accounts.first()
                FixedExpense.objects.create(
                    user=request.user,
                    name=name,
                    amount=amount,
                    due_day=due_day,
                    periodicity=periodicity,
                    pay_early_business_day=pay_early,
                    paying_account=paying_acc,
                )
            # Redirecionar para o dashboard usando a data do passo 1 (se existir)
            iso = request.session.get('onboarding_date')
            if iso:
                from datetime import datetime
                d = datetime.strptime(iso, '%Y-%m-%d').date()
                url = reverse_lazy('dashboard') + f"?month={d.month}&year={d.year}&onboarding={iso}"
            else:
                url = reverse_lazy('dashboard')
            from django.shortcuts import redirect
            return redirect(url)
        return self.render_to_response({'formset': formset, 'var_form': var_form})
