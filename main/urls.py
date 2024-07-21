from django.urls import path
from .views import RespondView,SurveyResponseUpdateView,update_events,get_events

urlpatterns = [
    path('respond/<int:survey_id>/', RespondView.as_view(), name='respond'),
    path('respond/<int:pk>/edit/', SurveyResponseUpdateView.as_view(), name='survey_response_update'),
    path('update-events/',update_events,name='update-events'),
    path('play-events/',update_events,name='update-events'),
    path('get-events/',get_events,name='get-events'),
]