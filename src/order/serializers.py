from rest_framework import serializers
from .models import Sale


# Create your selerializers here.
class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields ='__all__'