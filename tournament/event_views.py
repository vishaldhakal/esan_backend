from .models import Event, EventFAQ, EventNewsFeed, EventSponsor
from account.models import Organizer
from .serializers import EventFAQSerializer, EventNewsFeedSerializer, EventSponsorSerializer, EventSerializer,EventSmallSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        user = request.user

        # Check if the user is an organizer
        if user.role != "Organizer" or user.role != "Admin":
            return Response({"error": "Only organizers can create events"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        slug = request.POST.get('slug')
        event_thumbnail = request.FILES.get("event_thumbnail")
        event_thumbnail_alt_description = request.POST.get("event_thumbnail_alt_description")
        event_description = request.POST.get('event_description', '')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')
        print(event_thumbnail)
        organizer = Organizer.objects.get(user=user)

        event = Event.objects.create(
            organizer=organizer,
            event_name=event_name,
            event_description=event_description,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            event_thumbnail=event_thumbnail,
            event_thumbnail_alt_description=event_thumbnail_alt_description,
            slug=slug
        )
        event.save()
        return Response({"success": "Successfully created Event"})
    except Organizer.DoesNotExist:
        return Response({"error": "Organizer not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event(request):
    try:
        idd = request.POST.get("id")
        event = Event.objects.get(id=idd)
        user = request.user

        # Check if the user is the organizer of the event
        if event.organizer.user != user or user.role != "Admin":
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        slug = request.POST.get('slug')
        event_thumbnail = request.FILES.get('event_thumbnail')
        event_thumbnail_alt_description = request.POST.get("event_thumbnail_alt_description")
        event_description = request.POST.get('event_description')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')

        print(event_thumbnail)

        event.event_name = event_name
        event.slug = slug
        if event_thumbnail:
            event.event_thumbnail = event_thumbnail
        event.event_thumbnail_alt_description = event_thumbnail_alt_description
        event.event_description = event_description
        event.event_start_date = event_start_date
        event.event_end_date = event_end_date

        event.save()
        return Response({"success": "Successfully updated Event"})
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def event_list(request):
    user= request.user
    orgg = Organizer.objects.get(user=user)
    event = Event.objects.filter(organizer=orgg)
    serializers = EventSmallSerializer(event, many = True)
    return Response({
        "events": serializers.data
    })   

@api_view(["GET"])
def all_event_list(request):
    event = Event.objects.all()
    serializers = EventSmallSerializer(event, many = True)
    return Response({
        "events": serializers.data
    })   


@api_view(['GET'])
def event_detail(request):
    slug = request.GET.get('slug')
    event = Event.objects.get(slug = slug)
    event_serializer = EventSerializer(event)
    faq = EventFAQ.objects.filter(event = event)
    faq_serializer = EventFAQSerializer(faq, many = True)
    sponsor = EventSponsor.objects.filter(event = event)
    sponsor_serializer = EventSponsorSerializer(sponsor, many = True)
    return Response({
        'event': event_serializer.data,
        'faqs': faq_serializer.data,
        'sponsors': sponsor_serializer.data
    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_event(request):
    slug = request.GET.get("slug")
    event = Event.objects.get(slug=slug)
    event.delete()
    return Response({"success": "Event Deleted Successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_faq(request):
    slug = request.GET.get('slug')
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq = EventFAQ.objects.filter(event=event)
    faq_ser = EventFAQSerializer(faq,many=True)

    return Response({"FAQs": faq_ser.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_sponsor(request):
    slug = request.GET.get('slug')
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsors = EventSponsor.objects.filter(event=event)
    sponsors_ser = EventSponsorSerializer(sponsors,many=True)

    return Response({"sponsors": sponsors_ser.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_sponsor_detail(request):
    id = request.GET.get("id")
    sponsors = EventSponsor.objects.get(id=id)
    sponsors_ser = EventSponsorSerializer(sponsors)

    return Response({"sponsor_detail": sponsors_ser.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_faq(request):
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    slug = request.POST.get('slug')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq = EventFAQ.objects.create(
        event=event,
        value=value,
        heading=heading,
        detail=detail
    )
    faq.save()

    return Response({"success": "Event FAQ created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_faq(request):
    faq_id = request.POST.get('id')
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        faq = EventFAQ.objects.get(id=faq_id)
    except EventFAQ.DoesNotExist:
        return Response({"error": "Event FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq.heading = heading
    faq.detail = detail
    faq.save()

    return Response({"success": "Event FAQ updated successfully"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_faq(request):
    id = request.GET.get("id")
    event_faq = EventFAQ.objects.get(id=id)
    event_faq.delete()
    return Response({"success": "EventFAQ deleted successfully"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_news_feed(request):
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    slug = request.POST.get('slug')
    content = request.POST.get('content')
    
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    organizer = Organizer.objects.get(user=user)
    news_feed = EventNewsFeed.objects.create(
        event=event,
        content=content,
        user=organizer
    )
    news_feed.save()
    return Response({"success": "Event News Feed created successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_news_feed(request):
    slug = request.GET.get('slug')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feeds = EventNewsFeed.objects.filter(event=event)
    news_feeds_serializer = EventNewsFeedSerializer(news_feeds, many=True)

    return Response({"news_feeds": news_feeds_serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_news_feed(request):
    news_feed_id = request.GET.get('id')
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    content = request.POST.get('content')

    try:
        news_feed = EventNewsFeed.objects.get(id=news_feed_id)
    except EventNewsFeed.DoesNotExist:
        return Response({"error": "Event News Feed does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feed.content = content
    news_feed.save()

    return Response({"success": "Event News Feed updated successfully"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_news_feed(request):
    news_feed_id = request.GET.get('id')

    try:
        news_feed = EventNewsFeed.objects.get(id=news_feed_id)
    except EventNewsFeed.DoesNotExist:
        return Response({"error": "Event News Feed does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feed.delete()

    return Response({"success": "Event News Feed deleted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_sponsor(request):
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    slug = request.POST.get('slug')
    sponsor_name = request.POST.get('sponsor_name')
    sponsor_link = request.POST.get('sponsor_link')
    sponsorship_category = request.POST.get('sponsorship_category')
    order = int(request.POST.get('order'))
    sponsor_banner = request.FILES.get('sponsor_banner')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor = EventSponsor.objects.create(
        event=event,
        sponsor_name=sponsor_name,
        sponsorship_category=sponsorship_category,
        sponsor_banner=sponsor_banner,
        sponsor_link=sponsor_link,
        order=order,
    )
    sponsor.save()

    return Response({"success": "Event Sponsor created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_sponsor(request):
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    sponsor_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_link = request.POST.get('sponsor_link')
    sponsor_banner = request.FILES.get('sponsor_banner')
    order = int(request.POST.get('order'))

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.sponsor_name = sponsor_name
    sponsor.sponsor_link = sponsor_link
    sponsor.sponsorship_category = sponsorship_category
    sponsor.order = order

    if sponsor_banner:
        sponsor.sponsor_banner = sponsor_banner

    sponsor.save()

    return Response({"success": "Event Sponsor updated successfully"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_sponsor(request):
    sponsor_id = request.GET.get('id')

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.delete()

    return Response({"success": "Event Sponsor deleted successfully"})