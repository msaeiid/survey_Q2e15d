from django.core.validators import RegexValidator
from django.forms import ModelForm
from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from Agah.models import Responder, AnswerSheet, Interviewer, Question


class Responder_form(ModelForm):
    class Meta:
        model = Responder
        fields = ('firstname', 'lastname', 'city', 'mobile',)


class Answersheet_form(ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ('date', 'day',)

    def __init__(self, *args, **kwargs):
        super(Answersheet_form, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label='تاریخ', widget=AdminJalaliDateWidget(
            attrs={'placeholder': 'تاریخ', 'autocomplete': 'off'}))


class Interviewer_form(ModelForm):
    class Meta:
        model = Interviewer
        fields = ('code',)

    def clean(self):
        cleaned_data = self.cleaned_data
        if Interviewer.objects.filter(code=cleaned_data.get('code')).exists():
            return cleaned_data


class Question_form(forms.Form):


    def __init__(self,*args, **kwargs):
        super(Question_form, self).__init__()
        Q2 = kwargs.get('instance').get('Q2')
        Q3 = kwargs.get('instance').get('Q3')
        Q4 = kwargs.get('instance').get('Q4')
        Q4_1 = kwargs.get('instance').get('Q4_1')
        T1 = kwargs.get('instance').get('T1')
        T2 = kwargs.get('instance').get('T2')
        T3 = kwargs.get('instance').get('T3')
        regions = kwargs.get('instance').get('regions')

        # Q2
        self.fields['age_year'] = forms.IntegerField(required=True, min_value=1300, max_value=1400, validators=[
            RegexValidator(regex='^13[0-9]{2}$', message='بازه سنی 1300 تا 1399 میباشد')])
        # Q3
        marital_status_choices = [('', '')]
        for option in Q3.options.all():
            marital_status_choices.append((option.value, option.title))

        marital_status_choices = tuple(marital_status_choices)
        self.fields['marital_status'] = forms.ChoiceField(choices=marital_status_choices, required=True)

        # T1
        home_choices = [('', '')]
        for option in T1.options.all():
            home_choices.append((option.value, option.title))

        home_choices = tuple(home_choices)
        self.fields['home'] = forms.ChoiceField(choices=home_choices, required=True)

        # T3
        region_choices = [('', '')]
        for region in regions:
            region_choices.append((region.value, region.title))
        region_choices = tuple(region_choices)
        self.fields['region'] = forms.ChoiceField(choices=region_choices, required=True)

        # Q4
        self.fields['number_of_child'] = forms.IntegerField(min_value=0, max_value=100, required=False)

        # T2
        job_choices = []
        for option in T2.options.all():
            job_choices.append((option.value, option.title))
        job_choices = tuple(job_choices)
        self.fields['job'] = forms.MultipleChoiceField(choices=job_choices, widget=forms.CheckboxSelectMultiple,
                                                       required=True)

        # Q4_1
        gender_choices = (('', ''),
                          ('boy', 'پسر'),
                          ('girl', 'دختر'),)
        self.fields['first_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                             required=False)
        self.fields['first_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices, required=False)
        self.fields['first_child_age'] = forms.IntegerField(label='سن', required=False)

        self.fields['second_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                              required=False)
        self.fields['second_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices,
                                                               required=False)
        self.fields['second_child_age'] = forms.IntegerField(label='سن', required=False)

        self.fields['third_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                             required=False)
        self.fields['third_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices, required=False)
        self.fields['third_child_age'] = forms.IntegerField(label='سن', required=False)
