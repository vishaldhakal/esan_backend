from django.urls import path

from faq.views import FAQList

urlpatterns = [
    path('faq/', FAQList, name='faq-list'),
]