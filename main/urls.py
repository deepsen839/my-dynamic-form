from django.urls import path
from .views import RespondView,SurveyResponseUpdateView,add_form

urlpatterns = [
    path('respond/<int:survey_id>/', RespondView.as_view(), name='respond'),
    path('respond/<int:pk>/edit/', SurveyResponseUpdateView.as_view(), name='survey_response_update'),
    path('add-form/', add_form, name='add-form'),
]