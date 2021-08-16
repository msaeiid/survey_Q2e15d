from django.core.validators import RegexValidator
from django.forms import ModelForm
from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from Agah.models import Responder, AnswerSheet, Interviewer


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

    def __init__(self, *args, **kwargs):
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
        self.fields['number_of_child'] = forms.IntegerField(min_value=0, max_value=100, required=False, disabled=True)

        # T2
        job_choices = []
        for option in T2.options.all():
            job_choices.append((option.value, option.title))
        job_choices = tuple(job_choices)
        self.fields['job'] = forms.MultipleChoiceField(choices=job_choices, widget=forms.CheckboxSelectMultiple,
                                                       required=True)

        # Q4_1
        gender_choices = [('', '')]
        for gender in Q4_1.options.all():
            gender_choices.append((gender.value, gender.title))
        self.fields['first_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                             required=False, disabled=True)
        self.fields['first_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices, required=False,
                                                              disabled=True)
        self.fields['first_child_age'] = forms.IntegerField(label='سن', required=False, disabled=True)

        self.fields['second_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                              required=False, disabled=True)
        self.fields['second_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices,
                                                               required=False, disabled=True)
        self.fields['second_child_age'] = forms.IntegerField(label='سن', required=False, disabled=True)

        self.fields['third_child_year'] = forms.IntegerField(label='سال تولد', min_value=1300, max_value=1400,
                                                             required=False, disabled=True)
        self.fields['third_child_gender'] = forms.ChoiceField(label='جنسیت', choices=gender_choices, required=False,
                                                              disabled=True)
        self.fields['third_child_age'] = forms.IntegerField(label='سن', required=False, disabled=True)


class Brand_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Brand_form, self).__init__()
        brands = kwargs.get('instance').get('brands')
        question = kwargs.get('instance').get('question')
        brands_lst = []
        for brand in brands:
            brands_lst.append((brand.value, brand.title))
        brands_lst = tuple(brands_lst)
        if question.code == 'A1':
            self.fields['A1'] = forms.MultipleChoiceField(label='', choices=brands_lst, widget=forms.RadioSelect,
                                                          required=False)
        elif question.code == 'A2':
            self.fields['A2'] = forms.MultipleChoiceField(label='', choices=brands_lst,
                                                          widget=forms.CheckboxSelectMultiple, required=False)
        elif question.code == 'A4':
            self.fields['A4'] = forms.MultipleChoiceField(label='', choices=brands_lst,
                                                          widget=forms.CheckboxSelectMultiple, required=False)
        elif question.code == 'A6':
            self.fields['A6'] = forms.MultipleChoiceField(label='', choices=brands_lst,
                                                          widget=forms.CheckboxSelectMultiple, required=False)
        elif question.code == 'A7' or question.code == 'A8' or question.code == 'A9' or question.code == 'A10':
            counter = 0
            for brand in brands:
                counter += 1
                self.fields[f'{question.code}-{counter}'] = forms.IntegerField(label=brand.title, required=False)
                # self.fields[f'{question.code}-{counter}'].widget.attrs['placeholder'] = brand.title
                self.fields[f'{question.code}-{counter}'].widget.attrs['class'] = question.code
                self.fields[f'{question.code}-{counter}'].widget.attrs['brand'] = counter
                self.fields[f'{question.code}-{counter}'].widget.attrs['min'] = 0
                if question.code == 'A8':
                    self.fields[f'{question.code}-{counter}'].widget.attrs['readonly'] = "readonly"
        elif question.code == 'A11':
            priority_choices = (('', ''),
                                (1, 'اول'),
                                (2, 'دوم'),
                                (3, 'سوم'),)
            counter = 0
            for brand in brands:
                counter += 1
                self.fields[f'{question.code}-{counter}'] = forms.ChoiceField(label=brand.title,
                                                                              choices=priority_choices,
                                                                              required=False)
                self.fields[f'{question.code}-{counter}'].widget.attrs['brand'] = counter
                self.fields[f'{question.code}-{counter}'].widget.attrs['class'] = question.code
            pass
        elif question.code == 'A12':
            temp_choices = [('', ''), ]
            for option in question.options.all():
                temp_choices.append((option.value, option.title))
            counter = 0
            for brand in brands:
                counter += 1
                self.fields[f'{question.code}-{counter}'] = forms.ChoiceField(label=brand.title, choices=temp_choices,
                                                                              required=False)
                self.fields[f'{question.code}-{counter}'].widget.attrs['brand'] = counter
                self.fields[f'{question.code}-{counter}'].widget.attrs['class'] = question.code


class Sentence(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Sentence, self).__init__()
