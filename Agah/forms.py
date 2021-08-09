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


class Question_form(ModelForm):
    class Meta:
        model = Question
        fields = ('code',)

    def __init__(self, *args, **kwargs):
        super(Question_form, self).__init__(*args, **kwargs)
        question = kwargs.get('instance')
        if question.code == 'Q2':
            self.fields['age_year'] = forms.IntegerField(required=True, min_value=1300, max_value=1400, validators=[
                RegexValidator(regex='^13[0-9]{2}$', message='بازه سنی 1300 تا 1399 میباشد')])
        elif question.code == 'Q3' or question.code == 'T1' or question.code == 'T3':
            field_name = ''
            if question.code == 'Q3':
                field_name = 'marital_status'
            elif question.code == 'T1':
                field_name = 'home'
            elif question.code == 'T3':
                field_name = 'region'
            _choices = [('', '')]
            if question.code == 'T3':
                for region in kwargs.get('initial').get('regions'):
                    _choices.append((region.value, region.title))
            else:
                for option in question.options.all():
                    _choices.append((option.value, option.title))
            _choices = tuple(_choices)
            self.fields[field_name] = forms.ChoiceField(choices=_choices, required=True)
        elif question.code == 'Q4':
            self.fields['numer_of_child'] = forms.IntegerField(min_value=0, max_value=100, required=False)
        elif question.code == 'T2':
            _choices = []
            for option in question.options.all():
                _choices.append((option.value, option.title))
            _choices = tuple(_choices)
            self.fields['job'] = forms.MultipleChoiceField(choices=_choices, widget=forms.CheckboxSelectMultiple,
                                                           required=True)
            print('')
        elif question.code == 'Q4_1':
            gender_choices = (('', ''),
                              ('boy', 'پسر'),
                              ('girl', 'دختر'),)
            self.fields['first_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                                 required=False)
            self.fields['first_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices,required=False)
            self.fields['first_child_age'] = forms.IntegerField(label='سن', required=False)

            self.fields['second_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                                  required=False)
            self.fields['second_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices,required=False)
            self.fields['second_child_age'] = forms.IntegerField(label='سن', required=False)

            self.fields['third_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                                 required=False)
            self.fields['third_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices,required=False)
            self.fields['third_child_age'] = forms.IntegerField(label='سن', required=False)
