from django.urls import path
from .views import HealthCheck, FloodControlListCreate, FloodControlRetrieveUpdateDestroy, index

urlpatterns = [
    # Web UI
    path("", index, name="index"),
    
    # API endpoints
    path("api/health/", HealthCheck.as_view(), name="api-health"),
    path("api/floodcontrol/", FloodControlListCreate.as_view(), name="api-floodcontrol-list-create"),
    path("api/floodcontrol/<int:pk>/", FloodControlRetrieveUpdateDestroy.as_view(), name="api-floodcontrol-detail"),
]
