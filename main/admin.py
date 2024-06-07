from django.contrib import admin
from .forms import CustomSurveyForm
# Register your models here.
from .models import Survey,SurveyResponse
@admin.register(Survey)
class surveyAdmin(admin.ModelAdmin):
    fields = ['title','description','form',]


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    fields = ['survey','response']
    form = CustomSurveyForm

