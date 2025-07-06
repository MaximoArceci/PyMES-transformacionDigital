from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from .views import viewsets_dict
from django.contrib import admin

# Registrar automáticamente todos los modelos en la API
router = DefaultRouter()

for model_name, viewset in viewsets_dict.items():
    router.register(model_name.lower(), viewset)

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('/', include(router.urls)),  # API REST
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Esquema OpenAPI
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # UI Swagger
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]
