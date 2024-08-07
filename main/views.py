# surveyapp/views.py
from django.shortcuts import render, get_object_or_404,redirect

from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse
from dynamic_forms.views import DynamicFormMixin
from .models import Survey, SurveyResponse,storeevents
from .forms import CustomSurveyForm,CreateForm
from datetime import date
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
class CustomDynamicFormMixin(DynamicFormMixin):
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form_instance_pk = self.kwargs[self.form_pk_url_kwarg]
        self.form_instance = self._get_object_containing_form(form_instance_pk)
        json_data = getattr(self.form_instance, self.form_field)
        form.fields[self.response_field].replace_fields(json_data)  # Replace existing fields with form JSON
        # Populate the form with SurveyResponse data
        survey_response = self._get_survey_response()
        if survey_response:
            form.initial[self.response_field] = survey_response.response
        return form

    def form_valid(self, form):
        action = form.save(commit=False)
        setattr(action, self.response_form_fk_field, self.form_instance)
        action.save()
        return super().form_valid(form)

    def _get_survey_response(self):
        # Get the SurveyResponse for this form instance, if it exists
        survey_response = None
        if hasattr(self, 'object') and hasattr(self.object, 'surveyresponse'):
            survey_response = self.object.surveyresponse
        else:
            survey_response_pk = self.kwargs.get('survey_response_pk')
            if survey_response_pk:
                survey_response = get_object_or_404(SurveyResponse, pk=survey_response_pk)
        return survey_response



class RespondView(CustomDynamicFormMixin, CreateView):
    model = SurveyResponse
    fields = ['response']
    template_name = "respond.html"

    form_model = Survey
    form_field = "form"
    form_pk_url_kwarg = "survey_id"
    response_form_fk_field = "survey"
    response_field = "response"

    def get_success_url(self):
        return reverse('survey_detail', kwargs={"survey_id": self.form_instance.pk})



class SurveyResponseUpdateView(UpdateView):
    model = SurveyResponse
    form_class = CustomSurveyForm
    template_name = 'surveyresponse_update.html'

    def get_success_url(self):
        return reverse('survey_detail', kwargs={'pk': self.object.survey.pk})

    def get_object(self, queryset=None):
        return SurveyResponse.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        response_data = {}
        survey_instance = form.instance.survey
        form_configuration = survey_instance.form

        for field_config in form_configuration:
            field_name = field_config['name']
            field_label = field_config['label']
            value = form.cleaned_data[field_name]
            if isinstance(value, date):
                response_data[field_label] = value.strftime('%Y-%m-%d')
            else:
                response_data[field_label] = value
        
        form.instance.response = json.dumps(response_data)
        return super().form_valid(form)

@csrf_exempt
def update_events(request):
    if request.method=='POST':
        try:
            #json.loads convert double quote to single quote 
            #json does not accept single quote so to get that
            # we need to do json.dumps after json.loads
            events = request.body.decode('utf-8')#it converts to byte to string
            print(events)
            storeevents.objects.create(events=events)
            return JsonResponse({'msg':'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'error'})
@csrf_exempt
def get_events(request):
    if request.method=='POST':
        stored_events = storeevents.objects.all()
        # for events in stored_events:
        #     print(json.load(io.BytesIO(events.events.encode()))) 
        events = [json.loads(events.events) for events in stored_events]
        return JsonResponse({'events':events})
    return render(request,'player.html')

def add_form(request):
    create_form = CreateForm(request.POST or None)
    if request.method=='POST':
        if create_form.is_valid():
            create_form.save()
            print('2222222222')
    return render(request,'create_respond.html',{'create_form':create_form})             
