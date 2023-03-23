"""
Serializer for dataset APIs
"""



from rest_framework import serializers
from core.models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    """ Serializer for Datasets """

    class Meta:
        model = Dataset
        fields = ['id','title','price','link']
        read_only_fields = ['id']

class DatasetDetailSerializer(DatasetSerializer):
    """ Serializer for dataset detail view """
    class Meta(DatasetSerializer.Meta):
        fields = DatasetSerializer.Meta.fields + ['description']