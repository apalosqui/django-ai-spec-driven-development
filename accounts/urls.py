from django.urls import path
from .views import AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView


urlpatterns = [
    path('', AccountListView.as_view(), name='account_list'),
    path('novo/', AccountCreateView.as_view(), name='account_create'),
    path('<int:pk>/editar/', AccountUpdateView.as_view(), name='account_update'),
    path('<int:pk>/remover/', AccountDeleteView.as_view(), name='account_delete'),
]

