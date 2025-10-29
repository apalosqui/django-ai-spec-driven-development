"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from users.views import SignupView, EmailLoginView, EmailLogoutView
from planning.api import SalaryRuleViewSet, FixedExpenseViewSet, VariableBudgetViewSet
from cards.api import CreditCardViewSet, CardTransactionViewSet, CardInvoiceViewSet
from transactions.api import TransferViewSet, TransactionLogViewSet, ProjectionSnapshotViewSet
from accounts.api import AccountViewSet
from .views import DashboardView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', EmailLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('transactions/', include('transactions.urls')),
    path('perfil/', include('profiles.urls')),
]

# API routes (DRF)
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')

# Planning
router.register(r'salary-rules', SalaryRuleViewSet, basename='salary-rule')
router.register(r'fixed-expenses', FixedExpenseViewSet, basename='fixed-expense')
router.register(r'variable-budgets', VariableBudgetViewSet, basename='variable-budget')

# Cards
router.register(r'credit-cards', CreditCardViewSet, basename='credit-card')
router.register(r'card-transactions', CardTransactionViewSet, basename='card-transaction')
router.register(r'card-invoices', CardInvoiceViewSet, basename='card-invoice')

# Transfers / Logs / Snapshots
router.register(r'transfers', TransferViewSet, basename='transfer')
router.register(r'transaction-logs', TransactionLogViewSet, basename='transaction-log')
router.register(r'projection-snapshots', ProjectionSnapshotViewSet, basename='projection-snapshot')

urlpatterns += [
    path('api/', include(router.urls)),
]
