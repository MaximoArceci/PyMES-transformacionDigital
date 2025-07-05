# # filters.py
# import django_filters
# from .models import CampaignUsers, CampaignResources, Campaigns, CampaignCertifiers, ReassignmentRequests, ResourceResourceMappings, UserResourceMappings, Users
# from django.db.models import JSONField
# from django_filters.filters import CharFilter

# class UsersFilter(django_filters.FilterSet):
#     handle = CharFilter(field_name='handle', lookup_expr='exact')
#     name = CharFilter(field_name='name', lookup_expr='icontains')
#     email = CharFilter(field_name='email', lookup_expr='icontains')

#     class Meta:
#         model = Users
#         fields = [
#             'handle', 'name', 'email'
#         ]

# class UserResourceMappingsFilter(django_filters.FilterSet):
#     state = CharFilter(field_name='state', lookup_expr='icontains')
#     notes = CharFilter(field_name='notes', lookup_expr='icontains')

#     class Meta:
#         model = UserResourceMappings
#         fields = [
#             'campaign', 'certificant_id', 'resource', 'certifier', 'state', 'commited', 'notes'
#         ]

# class ResourceResourceMappingsFilter(django_filters.FilterSet):

#     class Meta:
#         model = ResourceResourceMappings
#         fields = [
#             'parent', 'child'
#         ]

# class ReassignmentRequestsFilter(django_filters.FilterSet):
#     type = CharFilter(field_name='type', lookup_expr='icontains')
#     state = CharFilter(field_name='state', lookup_expr='icontains')
#     created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
#     created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
#     updated_after = django_filters.DateFilter(field_name='updated_at', lookup_expr='gte')
#     updated_before = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')
#     notes = CharFilter(field_name='notes', lookup_expr='icontains')

#     class Meta:
#         model = ReassignmentRequests
#         fields = [
#             'campaign', 'emitter', 'receiver', 'certificant', 'type', 'state', 'created_at', 'updated_at', 'notes', 'created_after', 'created_before', 'updated_after', 'updated_before'
#         ]

# class CampaignUsersFilter(django_filters.FilterSet):
#     source_key = django_filters.CharFilter(field_name='source_key', lookup_expr='exact')
#     source_id = CharFilter(field_name='source_key__source_id', lookup_expr='exact')
#     object_id = CharFilter(field_name='source_key__object_id', lookup_expr='exact')
#     class Meta:
#         model = CampaignUsers
#         fields = [
#             'campaign', 'handle', 'name', 'source_key', 'source_id', 'object_id'
#         ]

# class CampaignCertifiersFilter(django_filters.FilterSet):
#     user = django_filters.CharFilter(field_name='user', lookup_expr='exact')
#     class Meta:
#         model = CampaignCertifiers
#         fields = [
#             'campaign', 'user'
#         ]

# class CampaignResourcesFilter(django_filters.FilterSet):
#     fields_Aplicacion = CharFilter(field_name='fields__Aplicacion', lookup_expr='icontains')
#     fields_risk = CharFilter(field_name='fields__risk', lookup_expr='exact')
#     name = django_filters.CharFilter(field_name='name', lookup_expr='exact')
#     type = django_filters.CharFilter(field_name='type', lookup_expr='icontains')
#     source_key = django_filters.CharFilter(field_name='source_key', lookup_expr='exact')
#     source_id = CharFilter(field_name='source_key__source_id', lookup_expr='exact')
#     object_id = CharFilter(field_name='source_key__object_id', lookup_expr='exact')

#     class Meta:
#         model = CampaignResources
#         fields = [
#             'name', 'campaign', 'type',
#             'fields_Aplicacion', 'fields_risk', 'source_key', 'source_id', 'object_id'
#         ]

# class CampaignsFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
#     type = django_filters.CharFilter(field_name='type', lookup_expr='icontains')
#     state = django_filters.CharFilter(field_name='state', lookup_expr='icontains')

#     start_after = django_filters.DateFilter(field_name='start', lookup_expr='gte')
#     end_before = django_filters.DateFilter(field_name='end', lookup_expr='lte')
#     start_before = django_filters.DateFilter(field_name='start', lookup_expr='lte')
#     end_after = django_filters.DateFilter(field_name='end', lookup_expr='gte')

#     class Meta:
#         model = Campaigns
#         fields = [
#             'name', 'closed_at', 'start', 'end', 'type', 'state',
#             'start_after', 'end_before', 'start_before', 'end_after'
#         ]