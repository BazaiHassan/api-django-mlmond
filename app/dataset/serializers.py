"""
Serializer for dataset APIs
"""



from rest_framework import serializers
from core.models import Dataset, Tag

class DatasetImageSerializer(serializers.ModelSerializer):
    """ Serializer to uploading image to the dataset """

    class Meta:
        model = Dataset
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image':{'required':'True'}}

class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tags """
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields=['id']

class DatasetSerializer(serializers.ModelSerializer):
    """ Serializer for Datasets """
    tags = TagSerializer(many=True, required=False)


    class Meta:
        model = Dataset
        fields = ['id','title','price','link']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, dataset):
        """ Handle getting or creating tag as needed """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user = auth_user, **tag,)
            dataset.tags.add(tag_obj)

        return dataset

    def create(self, validated_data):
        """ Create a dataset """
        tags = validated_data.pop('tags',[])
        dataset = Dataset.objects.create(**validated_data)
        self._get_or_create_tags(tags, dataset)
        return dataset

    def update(self, instance, validated_data):
        """ Update the dataset """
        tags = validated_data.pop('tags', None)
        
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class DatasetDetailSerializer(DatasetSerializer):
    """ Serializer for dataset detail view """
    class Meta(DatasetSerializer.Meta):
        fields = DatasetSerializer.Meta.fields + ['description']