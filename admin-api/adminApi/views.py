from rest_framework import viewsets
from django.apps import apps


if 'serializers_dict' not in globals():
    serializers_dict = {}
    from rest_framework import serializers
    for model in apps.get_models():
        # Filtra algunos modelos de Django internos si no quieres crear serializadores para ellos
        if not model._meta.app_label.startswith('django.contrib') and not model._meta.app_label.startswith('drf_spectacular'):
            class DynamicModelSerializer(serializers.ModelSerializer):
                class Meta:
                    model = model
                    fields = '__all__'
            serializers_dict[model.__name__] = DynamicModelSerializer

models = apps.get_models()
viewsets_dict = {}
for model in models:
    serializer_class = serializers_dict.get(model.__name__)
    if serializer_class:
        class GenericViewSet(viewsets.ModelViewSet):
            queryset = model.objects.all()
            serializer_class = serializer_class
        viewsets_dict[model.__name__] = GenericViewSet

