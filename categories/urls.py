from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView


urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('nova/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/editar/', CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/remover/', CategoryDeleteView.as_view(), name='category_delete'),
]

