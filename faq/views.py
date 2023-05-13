from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from faq.models import FAQ
from faq.serializers import FAQSerializer

# Create your views here.

@api_view(["POST"])
def Create_FAQ(request):
    heading = request.POST['heading']
    detail = request.POST['detail']
    value =request.POST['value']

    faq = FAQ(
        heading = heading,
        detail = detail,
        value = value
    )
    faq.save()
    return Response({"FAQ created successfully"})

@api_view(["PUT"])
def Update_FAQ(request, id):
    faq = FAQ.objects.get(id=id )
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')
    value =request.POST.get('value')

    faq.heading = heading
    faq.detail = detail
    faq.value = value

    faq.save()
    return Response({"FAQ Updated Successfully"})


@api_view(["GET"])
def FAQList(request):
    faq = FAQ.objects.all()
    serializers = FAQSerializer(faq, many = True)
    return Response({
        "FAQs": serializers.data
    })


@api_view(["DELETE"])
def delete_faq(request, id):
    faq = FAQ.objects.get(id=id )
    faq.delete()
    return Response({"FAQ Deleted Successfully"})


