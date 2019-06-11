from django.contrib import admin
from bot.models.tables import (
    User,
    City,
    Resume,
    Job,
    Statistics,
    JobDialog,
    ResumeDialog
)

admin.site.register(User)
admin.site.register(City)
admin.site.register(Statistics)
admin.site.register(JobDialog)
admin.site.register(ResumeDialog)


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
