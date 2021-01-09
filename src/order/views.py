from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SaleSerializer
from .models import Sale


# Create your views here.
def order_sale_list(request):
    template_name = 'order/sale_list.html'
    context = {
        'title': "Order",
    }
    return render(request, template_name, context)



@api_view(['GET'])
def api_order_sale_list(request):
    sales = Sale.objects.all().order_by('-id')
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def api_order_sale_save(request):
    serializer = SaleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
