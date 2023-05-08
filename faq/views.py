from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from faq.models import FAQ
from faq.serializers import FAQSerializer

# Create your views here.
@api_view(["GET"])
def FAQList(request):
    faq = FAQ.objects.all()
    serializers = FAQSerializer(faq, many = True)
    return Response({
        "FAQs": serializers.data
    })

    