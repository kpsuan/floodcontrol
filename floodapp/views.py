from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FloodControl
from .serializers import FloodControlSerializer

class HealthCheck(APIView):
    """
    API endpoint for health checks
    """
    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)

class FloodControlListCreate(generics.ListCreateAPIView):
    """
    API endpoint for listing all flood control projects and creating new ones
    GET: Returns all projects
    POST: Creates a new project
    """
    queryset = FloodControl.objects.all()
    serializer_class = FloodControlSerializer

class FloodControlRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific flood control project
    GET: Returns a specific project
    PUT/PATCH: Updates a specific project
    DELETE: Deletes a specific project
    """
    queryset = FloodControl.objects.all()
    serializer_class = FloodControlSerializer

# Web UI view (keeping this for the HTML interface)
def index(request):
    """
    Web interface for managing flood control projects
    """
    if request.method == "POST":
        if "delete_id" in request.POST:
            project = get_object_or_404(FloodControl, pk=request.POST["delete_id"])
            project.delete()
            return redirect("/")
        
        FloodControl.objects.create(
            description=request.POST["description"],
            location=request.POST["location"],
            contractor=request.POST["contractor"],
            cost=float(request.POST["cost"]),
            completion_date=request.POST["completion_date"],
        )
        return redirect("/")
    
    projects = FloodControl.objects.all()
    return render(request, "index.html", {"projects": projects})
