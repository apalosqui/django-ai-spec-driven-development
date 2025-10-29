from django.contrib import admin

from .models import Transaction, Transfer, TransactionLog, ProjectionSnapshot

admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(TransactionLog)
admin.site.register(ProjectionSnapshot)
