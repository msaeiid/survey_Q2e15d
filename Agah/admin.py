from django.contrib import admin

from Agah.models import City, Responder, Interviewer, Question, Survey, AnswerSheet, Option, Answer, Region, \
    Child, Limit


class AnswerSheetCustom(admin.ModelAdmin):
    list_display = (
        'interviewer', 'responser', 'survey', 'date', 'day', 'total_point',
        'social_class',)


class CityCustom(admin.ModelAdmin):
    list_display = ('name', 'population', 'is_important',)
    list_editable = ('population', 'is_important',)


class InterviewerCustom(admin.ModelAdmin):
    list_display = ('name', 'code',)


class ResponderCustom(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'city', 'mobile',)
    list_editable = ('city', 'mobile',)


class SurveyCustom(admin.ModelAdmin):
    list_display = ('title',)


class QuestionCustom(admin.ModelAdmin):
    list_display = ('survey', 'code', 'title', 'type', 'previous_question', 'next_question',)
    list_editable = ('previous_question', 'next_question', 'type',)


class OptionCustom(admin.ModelAdmin):
    list_display = ('question', 'title', 'value', 'point',)
    list_editable = ('value', 'point',)


class AnswerCustom(admin.ModelAdmin):
    list_display = ('answersheet', 'question', 'option', 'answer', 'point',)


class RegionCustom(admin.ModelAdmin):
    list_display = ('city', 'question', 'title', 'value', 'point',)
    list_editable = ('question', 'title', 'value', 'point',)


class ChildCustom(admin.ModelAdmin):
    list_display = ('responder', 'gender', 'birthday_year',)


class LimitCustom(admin.ModelAdmin):
    list_display = ('marital_status', 'age', 'maximum', 'capacity',)


admin.site.register(City, CityCustom)
admin.site.register(Interviewer, InterviewerCustom)
admin.site.register(Responder, ResponderCustom)
admin.site.register(Survey, SurveyCustom)
admin.site.register(Question, QuestionCustom)
admin.site.register(AnswerSheet, AnswerSheetCustom)
admin.site.register(Option, OptionCustom)
admin.site.register(Answer, AnswerCustom)
admin.site.register(Region, RegionCustom)
admin.site.register(Child, ChildCustom)
admin.site.register(Limit, LimitCustom)

# Register your models here.
