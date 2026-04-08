from django.shortcuts import render
from rest_framework import permissions, viewsets, generics

from supplier.models import Supplier
from supplier.serializers import SupplierSerializer

class SupplierApiView(generics.ListAPIView):

    queryset = Supplier.objects.all().order_by("created_at")
    serializer_class = SupplierSerializer
