from .import views
from django.urls import path
from .views import submit_testimonial,verify_testimonial,delete_testimonial,update_testimonial,testimonials,all_testimonials


urlpatterns = [
    path('submit-testimonial/', submit_testimonial, name='submit_testimonial'),
    path('verify-testimonial/', verify_testimonial, name='verify_testimonial'),
    path('delete-testimonial/', delete_testimonial, name='delete_testimonial'),
    path('testimonials/', testimonials, name='testimonials'),
    path('all-testimonials/', all_testimonials, name='testimonials'),
]
