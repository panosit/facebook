from django.contrib import admin
from .models import UserProfile, Poke


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'concentration', 'house', 'class_year')
    search_fields = ('user__username', 'user__email')


@admin.register(Poke)
class PokeAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    list_filter = ('created_at',)
