
from django.db import models
from dynamic_forms.models import FormField, ResponseField

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    form = FormField()
    def __str__(self) -> str:
        return f"{self.title}"



class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE) # Optional
    response = ResponseField()
    created_at = models.DateTimeField(auto_now_add=True)


class storeevents(models.Model):
    events = models.TextField()    
