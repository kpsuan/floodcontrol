from django.db import models

class FloodControl(models.Model):
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    contractor = models.CharField(max_length=100)
    cost = models.FloatField()
    completion_date = models.DateField()

    def __str__(self):
        return f"{self.description} ({self.location})"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "location": self.location,
            "contractor": self.contractor,
            "cost": self.cost,
            "completion_date": self.completion_date.strftime("%Y-%m-%d"),
        }
