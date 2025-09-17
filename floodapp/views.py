from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FloodControl
from datetime import datetime
import json

# Health endpoint
def health_check(request):
    return JsonResponse({"status": "healthy"}, status=200)

# Get all projects
def get_floodcontrol(request):
    items = FloodControl.objects.all()
    return JsonResponse([i.to_dict() for i in items], safe=False)

# Create project
def create_floodcontrol(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item = FloodControl.objects.create(
            description=data["description"],
            location=data["location"],
            contractor=data["contractor"],
            cost=data["cost"],
            completion_date=datetime.strptime(data["completion_date"], "%Y-%m-%d").date(),
        )
        return JsonResponse(item.to_dict(), status=201)

# Get single project
def get_floodcontrol_item(request, id):
    item = get_object_or_404(FloodControl, pk=id)
    return JsonResponse(item.to_dict())

# Update project
def update_floodcontrol(request, id):
    item = get_object_or_404(FloodControl, pk=id)
    if request.method == "PUT":
        data = json.loads(request.body)
        item.description = data.get("description", item.description)
        item.location = data.get("location", item.location)
        item.contractor = data.get("contractor", item.contractor)
        item.cost = data.get("cost", item.cost)
        if "completion_date" in data:
            item.completion_date = datetime.strptime(data["completion_date"], "%Y-%m-%d").date()
        item.save()
        return JsonResponse(item.to_dict())

# Delete project
def delete_floodcontrol(request, id):
    item = get_object_or_404(FloodControl, pk=id)
    if request.method == "DELETE":
        item.delete()
        return JsonResponse({"message": "Flood control project deleted"})

# Web UI
def index(request):
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
