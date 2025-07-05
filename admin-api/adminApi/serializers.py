from rest_framework import serializers
from django.apps import apps
from .models import CampaignUsers, CampaignResources, Campaigns, CampaignCertifiers, ReassignmentRequests, ResourceResourceMappings, UserResourceMappings, Users
from django.db import models as django_models
# Obtiene todos los modelos de la aplicación
models = apps.get_models()

# Crea dinámicamente un serializer para cada modelo
serializers_dict = {}

for model in models:
    class Meta:
        model = model
        fields = '__all__'

    serializer_class = type(
        f"{model.__name__}Serializer", (serializers.ModelSerializer,), {"Meta": Meta})
    serializers_dict[model.__name__] = serializer_class

# class UsersSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla Users con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = Users
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(f"/api/users/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }

# class UserResourceMappingsSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla UserResourceMappings con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = UserResourceMappings
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(
#             f"/api/userresourcemappings/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }

# class ResourceResourceMappingsSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla ResourceResourceMappings con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = ResourceResourceMappings
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(
#             f"/api/resourceresourcemappings/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }

# class ReassignmentRequestsSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla ReassignmentRequests con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = ReassignmentRequests
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(
#             f"/api/reassignmentrequests/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }

# class CampaignUsersSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla CampaignUsers con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = CampaignUsers
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(f"/api/campaignusers/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }

# class CampaignCertifierSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla CampaignCertifiers con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = CampaignCertifiers
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(
#             f"/api/campaigncertifiers/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }


# class CampaignSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla Campaigns con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()

#     class Meta:
#         model = Campaigns
#         fields = [f.name for f in model._meta.fields] + ['links']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(f"/api/campaigns/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }


# class CampaignResourcesSerializer(serializers.ModelSerializer):
#     """
#     Serializer para la tabla CampaignResources con enlaces HATEOAS.
#     """
#     links = serializers.SerializerMethodField()
#     campaign_link = serializers.SerializerMethodField()

#     class Meta:
#         model = CampaignResources
#         fields = [f.name for f in model._meta.fields] + \
#             ['links', 'campaign_link']

#     def get_links(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return {}

#         base_url = request.build_absolute_uri(
#             f"/api/campaignresources/{obj.pk}/")
#         return {
#             "self": base_url,
#             "update": base_url,
#             "delete": base_url
#         }

#     def get_campaign_link(self, obj):
#         request = self.context.get('request')
#         if not request:
#             return None

#         return request.build_absolute_uri(f"/api/campaigns/{obj.campaign_id}/")

# class CampaignConfigSerializer(serializers.Serializer):
#     """Serializador para la configuración de la campaña."""
#     type = serializers.CharField(default="PEOPLE")
#     state = serializers.CharField(default="IN_PROGRESS")
#     name = serializers.CharField(default="Prueba diferencial y subniveles")
#     start = serializers.CharField(
#         help_text="Fecha y hora de inicio de la campaña (ISO 8601 con 'Z' al final, ej. 2025-06-07T17:30:00.000000Z)"
#     )
#     end = serializers.CharField(
#         help_text="Fecha y hora de fin de la campaña (ISO 8601 con 'Z' al final, ej. 2025-07-07T17:30:00.000000Z)"
#     )

# class CertifierConfigSerializer(serializers.Serializer):
#     """Serializador para la configuración del certificador."""
#     name = serializers.CharField(default="User test")
#     fields = serializers.JSONField(default=dict)
#     source_key = serializers.JSONField(default=dict)
#     handle = serializers.CharField(default="CERT_TEST")

# class UsersConfigSerializer(serializers.Serializer):
#     """Serializador para la configuración de los usuarios."""
#     handle_prefix = serializers.CharField(default="usuario_a_")
#     name_prefix = serializers.CharField(default="Usuario A ")
#     fields = serializers.JSONField(default=dict)
#     source_key = serializers.JSONField(default=dict)

# class ResourceTypeOptions(django_models.TextChoices):
#     ROLE = 'ROLE', 'Role' # El segundo valor es el display name (opcional pero recomendado)
#     PERMISSION = 'PERMISSION', 'Permission'

# class ResourceConfigSerializer(serializers.Serializer):
#     """Serializador para la configuración de los recursos."""
#     name_prefix = serializers.CharField(default="Recurso ")
#     source_key = serializers.JSONField(default=dict)
#     resname1 = serializers.CharField(required=False, allow_blank=True)
#     resname2 = serializers.CharField(required=False, allow_blank=True)
#     resname3 = serializers.CharField(required=False, allow_blank=True)
#     owner = serializers.IntegerField(required=False)
#     role_type = serializers.CharField(required=False, allow_blank=True)
#     description = serializers.CharField(default="Recurso de prueba", required=False, allow_blank=True)
    
#     # Aquí es donde cambias el campo 'type' a un ChoiceField con tus opciones de enum
#     type = serializers.ChoiceField(
#         choices=ResourceTypeOptions.choices,
#         default=ResourceTypeOptions.ROLE,
#         help_text="Tipo de recurso, puede ser 'ROLE' o 'PERMISSION'."
#     )
    
#     first_resource_risk = serializers.CharField(default="8")
#     else_resource_risk = serializers.CharField(default="1")

# class ImportCaseConfigSerializer(serializers.Serializer):
#     """
#     Serializador principal para la configuración del script de importación de casos.
#     Define la estructura completa del JSON de entrada.
#     """
#     API_BASE = serializers.URLField(help_text="URL base de la API, ej. http://10.1.2.14/admin/api")
#     campaign = CampaignSerializer()
#     certifier = CertifierConfigSerializer()
#     users = UsersConfigSerializer()
#     resource = ResourceConfigSerializer()

#     class Meta:
#         ref_name = "ImportCaseConfig"
