from django.urls import path
from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
)


urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('nova/', TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/editar/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('<int:pk>/remover/', TransactionDeleteView.as_view(), name='transaction_delete'),
]

