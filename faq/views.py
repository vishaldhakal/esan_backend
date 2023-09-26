from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes)
from faq.models import FAQ
from faq.serializers import FAQSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_faq(request):
    user = request.user
    if user.role == 'Admin':
        heading = request.POST['heading']
        detail = request.POST['detail']
        value =request.POST['value']

        faq = FAQ.objects.create(
            heading = heading,
            detail = detail,
            value = value
        )
        faq.save()
        return Response({"success":"FAQ created successfully"})
    else:
        return Response({"error":"Unauthourized for creating FAQ"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_faq(request):
    user = request.user
    idd = int(request.GET.get("id"))
    if user.role == 'Admin':
        faq = FAQ.objects.get(id=idd )
        heading = request.POST.get('heading')
        detail = request.POST.get('detail')

        faq.heading = heading
        faq.detail = detail

        faq.save()
        return Response({"success":"FAQ Updated Successfully"})
    else:
        return Response({"error":"Unauthourized for updating  FAQ"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def faq_list(request):
    faq = FAQ.objects.all()
    serializers = FAQSerializer(faq, many = True)
    return Response({
        "FAQs": serializers.data
    },status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_faq(request):
    user = request.user
    idd = int(request.GET.get("id"))
    if user.role == 'Admin':
        faq = FAQ.objects.get(id=idd )
        faq.delete()
        return Response({"success":"FAQ Deleted Successfully"})
    else:
        return Response({"error":"Unauthourized for deleting  FAQ"}, status=status.HTTP_401_UNAUTHORIZED)



