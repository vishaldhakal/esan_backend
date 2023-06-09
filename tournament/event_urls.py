from django.urls import path
from . import event_views

urlpatterns = [
    path('create-event/', event_views.create_event, name='create_event'),
    path('update-event/', event_views.update_event, name='update_event'),
    path('all-events/', event_views.all_event_list, name='all_event_list'),
    path('events/', event_views.event_list, name='events'),
    path('event-detail/', event_views.event_detail, name='event_detail'),
    path('delete-event/', event_views.delete_event, name='delete_event'),
    path('get-event-faqs/', event_views.get_event_faq, name='get_event_faq'),
    path('create-event-faq/', event_views.create_event_faq, name='create_event_faq'),
    path('update-event-faq/', event_views.update_event_faq, name='update_event_faq'),
    path('delete-event-faq/', event_views.delete_event_faq, name='delete_event_faq'),
    path('create-event-news-feed/', event_views.create_event_news_feed, name='create_event_news_feed'),
    path('get-event-news-feed/', event_views.get_event_news_feed, name='get_event_news_feed'),
    path('update-event-news-feed/', event_views.update_event_news_feed, name='update_event_news_feed'),
    path('delete-event-news-feed/', event_views.delete_event_news_feed, name='delete_event_news_feed'),
    path('get-event-sponsors/', event_views.get_event_sponsor, name='get_event_sponsor'),
    path('get-event-sponsor-detail/', event_views.get_event_sponsor_detail, name='get_event_sponsor_detail'),
    path('create-event-sponsor/', event_views.create_event_sponsor, name='create_event_sponsor'),
    path('update-event-sponsor/', event_views.update_event_sponsor, name='update_event_sponsor'),
    path('delete-event-sponsor/', event_views.delete_event_sponsor, name='delete_event_sponsor'),
]
