from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView
from Agah.forms import Interviewer_form, Answersheet_form, Responder_form, Question_form
from Agah.models import Survey, Question, AnswerSheet, Interviewer


class Survey_View(DetailView):
    model = Survey
    template_name = 'Survey.html'
    context_object_name = 'Survey'



@csrf_protect
def Personal(request, pk):
    answersheet = request.session.get('answersheet', None)
    survey = get_object_or_404(Survey, pk=pk)
    Q1 = get_object_or_404(Question, previous_question=None)
    if request.method == 'GET':
        if answersheet is None:
            interviewer_frm = Interviewer_form(request.GET)
            answersheet_frm = Answersheet_form(request.GET)
            responder_frm = Responder_form(request.GET)
        else:
            import jdatetime
            answersheet = get_object_or_404(AnswerSheet, pk=answersheet)
            # TODO: here i should convert date again
            answersheet.date = str(
                jdatetime.date.fromgregorian(year=answersheet.date.year, month=answersheet.date.month,
                                             day=answersheet.date.day))
            #
            interviewer_frm = Interviewer_form(request.POST, instance=answersheet.interviewer)
            answersheet_frm = Answersheet_form(request.POST, instance=answersheet)
            responder_frm = Responder_form(request.POST, instance=answersheet.responser)
        context = {'survey': survey, 'interviewer_frm': interviewer_frm, 'answersheet_frm': answersheet_frm,
                   'responder_frm': responder_frm, 'Q1': Q1}
        return render(request=request, template_name='Personal.html', context=context)
    else:
        if answersheet is None:
            interviewer_frm = Interviewer_form(request.POST)
            answersheet_frm = Answersheet_form(request.POST)
            responder_frm = Responder_form(request.POST)
            if interviewer_frm.is_valid() and answersheet_frm.is_valid() and responder_frm.is_valid():
                interviwer = get_object_or_404(Interviewer, code=interviewer_frm.cleaned_data.get('code'))
                responder = responder_frm.save()
                answersheet = answersheet_frm.save(commit=False)
                answersheet.responser = responder
                answersheet.survey = survey
                answersheet.interviewer = interviwer
                answersheet.save()
            else:
                context = {'survey': survey, 'interviewer_frm': interviewer_frm, 'answersheet_frm': answersheet_frm,
                           'responder_frm': responder_frm, 'Q1': Q1}
                return render(request=request, template_name='Personal.html', context=context)
        else:
            answersheet = get_object_or_404(AnswerSheet, pk=answersheet)
            interviewer_frm = Interviewer_form(request.POST)
            answersheet_frm = Answersheet_form(request.POST)
            responder_frm = Responder_form(request.POST)
            if interviewer_frm.is_valid() and answersheet_frm.is_valid() and responder_frm.is_valid():
                if answersheet_frm.has_changed():
                    answersheet.date = answersheet_frm.cleaned_data.get('date')
                    answersheet.day = answersheet_frm.cleaned_data.get('day')
                    answersheet.save()
                if interviewer_frm.has_changed():
                    answersheet.interviewer_id = interviewer_frm.cleaned_data.get('code')
                    answersheet.interviewer.save()
                if responder_frm.has_changed():
                    answersheet.responser.firstname = responder_frm.cleaned_data.get('firstname')
                    answersheet.responser.lastname = responder_frm.cleaned_data.get('lastname')
                    answersheet.responser.mobile = responder_frm.cleaned_data.get('mobile')
                    answersheet.responser.city_id = responder_frm.cleaned_data.get('city')
                    answersheet.responser.save()
        request.session['answersheet'] = answersheet.pk
        request.session['survey'] = survey.pk
        request.session['question'] = Q1.next_question.pk
        return redirect(reverse('social'))


def interviwer_name(request):
    if request.method == 'GET' and request.is_ajax:
        try:
            interviwer = get_object_or_404(Interviewer, code=int(request.GET.get('code')))
        except:
            context = {}
            return JsonResponse(context, status=404)
        else:
            context = {'name': interviwer.name}
        return JsonResponse(context, status=200)


@csrf_protect
def Social(request):
    answersheet = request.session.get('answersheet')
    answersheet = get_object_or_404(AnswerSheet, pk=answersheet)
    Q2 = get_object_or_404(Question, pk=request.session['question'])
    Q3 = Q2.next_question
    Q4 = Q3.next_question
    Q4_1 = Q4.next_question
    T1 = Q4_1.next_question
    T2 = T1.next_question
    T3 = T2.next_question
    if request.method == 'GET':
        Q2_form = Question_form(request.GET, instance=Q2)
        Q3_form = Question_form(request.GET, instance=Q3)
        Q4_form = Question_form(request.GET, instance=Q4)
        Q4_1_form = Question_form(request.GET, instance=Q4_1)
        T1_from = Question_form(request.GET, instance=T1)
        T2_form = Question_form(request.GET, instance=T2)
        T3_from = Question_form(request.GET, instance=T3,
                                initial={'regions': T3.regions.filter(city=answersheet.responser.city)})
        context = {'Q2': Q2, 'Q2_form': Q2_form,
                   'Q3': Q3, 'Q3_form': Q3_form,
                   'Q4': Q4, 'Q4_form': Q4_form,
                   'Q4_1': Q4_1, 'Q4_1_form': Q4_1_form,
                   'T1': T1, 'T1_from': T1_from,
                   'T2': T2, 'T2_form': T2_form,
                   'T3': T3, 'T3_from': T3_from,
                   'answersheet': answersheet,
                   }
        return render(request, 'Social.html', context)
    else:
        print('')
        pass
# Create your views here.
