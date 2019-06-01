from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='main_page/main_page.html'),
         name='bot_view'),
]
