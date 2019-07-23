from django.contrib import admin
from bot.models.tables import (
    User,
    City,
    Resume,
    Job,
)

admin.site.register(User)
admin.site.register(City)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'position')
    date_hierarchy = 'created'
    list_filter = ('moderation',)
    search_fields = ['category']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'position')
    date_hierarchy = 'created'
    list_filter = ('moderation',)
    search_fields = ['category']
