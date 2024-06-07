from django import forms
from .models import SurveyResponse
import json

class CustomSurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        survey_instance = self.instance.survey
        form_configuration = survey_instance.form

        for field_config in form_configuration:
            field_name = field_config['name']
            field_type = field_config['type']
            field_label = field_config['label']

            if field_type == 'checkbox-group':
                choices = [(option['value'], option['label']) for option in field_config['options']]
                self.fields[field_name] = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple(), label=field_label)
            elif field_type == 'date':
                self.fields[field_name] = forms.DateField(label=field_label, widget=forms.DateInput(attrs={'type': 'date'}))
            elif field_type == 'hidden':
                self.fields[field_name] = forms.CharField(widget=forms.HiddenInput(), label=field_label)
            elif field_type == 'number':
                self.fields[field_name] = forms.DecimalField(label=field_label)
            elif field_type == 'radio-group':
                choices = [(option['value'], option['label']) for option in field_config['options']]
                self.fields[field_name] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect(), label=field_label)
            elif field_type == 'select':
                choices = [(option['value'], option['label']) for option in field_config['options']]
                self.fields[field_name] = forms.ChoiceField(choices=choices, label=field_label)
            elif field_type == 'text' or field_type == 'email':
                self.fields[field_name] = forms.CharField(label=field_label)
            elif field_type == 'textarea':
                self.fields[field_name] = forms.CharField(label=field_label, widget=forms.Textarea())

        if self.instance.pk:
            print(self.instance.pk)
            # response = json.loads(self.instance.response)
            for field_config in form_configuration:
                field_name = field_config['name']
                field_label = field_config['label']

                print(self.instance.response)
                # if field_label in response:
                self.fields[field_name].initial = self.instance.response.get(field_label)

    class Meta:
        model = SurveyResponse
        fields = []


