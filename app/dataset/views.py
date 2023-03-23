"""
Views for the Dataset API
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Dataset
from dataset import serializers

class DatasetViewSet(viewsets.ModelViewSet):
    """ view for manage dataset API """
    serializer_class = serializers.DatasetDetailSerializer
    queryset = Dataset.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ retrieve datasets for authenticated users """
        return self.queryset.filter(user=self.request.user).order_by('_id')

    def get_serializer_calss(self):
        """ Return the serializer class for request """
        if self.action == 'list':
            return serializers.DatasetSerializer
        return self.serializer_calss

    def perform_create(self, serializer):
        """ create a new dataset """
        serializer.save(user=self.request.user)