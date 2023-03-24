"""
Views for the Dataset API
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Dataset, Tag
from dataset import serializers

@extend_schema_view(
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tags IDs to filter'
            )
        ]
    )
)
class DatasetViewSet(viewsets.ModelViewSet):
    """ view for manage dataset API """
    serializer_class = serializers.DatasetSerializer
    queryset = Dataset.objects.all()
    authentication_classes = [TokenAuthentication]

    def _params_to_ints(self, qs):
        """ Convert a list of strings to integers """
        return [int(str_id) for str_id in qs.split(',')]
    
    def get_permissions(self):
        """ Modifying GET method """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


    def get_queryset(self):
        """ retrieve datasets for authenticated users """
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if self.request.method == 'GET':
            return queryset.order_by('-id').distinct()

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """ Return the serializer class for request """
        if self.action == 'list':
            return serializers.DatasetSerializer
        elif self.action == 'upload_image':
            return serializers.DatasetImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ create a new dataset """
        serializer.save(user=self.request.user)


    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to dataset """
        dataset = self.get_object()
        serializer = self.get_serializer(dataset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to dataset'
            )
        ]
    )
)
class TagViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    """ Manage tags in the db """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ filter queryset for authenticated users """
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(dataset__isnull=False)
        return queryset.filter(user = self.request.user).order_by('-name').distinct()