from django.urls import path
from faq.views import create_faq, delete_faq, faq_list, update_faq  

urlpatterns = [
    path('create-faq/', create_faq, name='create_faq'),
    path('update-faq/', update_faq, name='update_faq'),
    path('faq-list/', faq_list, name='faq_list'),
    path('delete-faq/', delete_faq, name='delete_faq'),
]
