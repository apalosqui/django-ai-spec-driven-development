from django.conf import settings
from django.db import models


class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name', 'type')
        ordering = ['type', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
