from django.contrib import admin

# Register your models here.
from .models import Article  # Załóżmy, że model nazywa się Article

# Rejestracja modelu w panelu administracyjnym
admin.site.register(Article)