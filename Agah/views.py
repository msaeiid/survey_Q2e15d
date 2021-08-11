from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView
from Agah.forms import Interviewer_form, Answersheet_form, Responder_form, Question_form
from Agah.models import Survey, Question, AnswerSheet, Interviewer, Limit, Answer, Child


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


def check_age(age):
    if 18 <= age <= 24:
        return 1
    elif 25 <= age <= 29:
        return 2
    elif 30 <= age <= 34:
        return 3
    elif 35 <= age <= 39:
        return 4
    elif 40 <= age <= 44:
        return 5
    elif 45 <= age <= 49:
        return 6
    elif 50 <= age <= 54:
        return 7
    elif 55 <= age <= 59:
        return 8
    elif 60 <= age < 64:
        return 9
    else:
        return 0


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
        form = Question_form(request.GET,
                             instance={'Q2': Q2, 'Q3': Q3, 'Q4': Q4, 'Q4_1': Q4_1, 'T1': T1, 'T2': T2, 'T3': T3,
                                       'regions': T3.regions.filter(city=answersheet.responser.city)})
        context = {'Q2': Q2, 'Q3': Q3, 'Q4': Q4, 'Q4_1': Q4_1, 'T1': T1, 'T2': T2, 'T3': T3, 'answersheet': answersheet,
                   'form': form}
        return render(request, 'Social.html', context)
    else:
        marital_status = int(request.POST.get('marital_status'))
        age = int(request.POST.get('age'))
        age_category = check_age(age)
        del age
        if marital_status == 0 or age_category == 0:
            answersheet.delete()
            print('full')
            # TODO redirect to end with message...
        if Limit.objects.filter(marital_status=marital_status, age=age_category).exists():
            limit = Limit.objects.get(marital_status=marital_status, age=age_category)
            if not limit.check_for_capacity():
                answersheet.delete()
                print('full')
                # TODO redirect to end with message...

        # Q2 save answer...
        answer = None
        if Answer.objects.filter(question=Q2, answersheet=answersheet).exists():
            answer = Answer.objects.get(question=Q2, answersheet=answersheet)
            answer.answer = age_category
            answer.point = Q2.options.get(value=age_category).point
        else:
            answer = Answer(question=Q2, answersheet=answersheet, answer=age_category,
                            point=Q2.options.get(value=age_category).point)
        answer.save()

        # Q3 save answer...
        if Answer.objects.filter(question=Q3, answersheet=answersheet).exists():
            answer = Answer.objects.get(question=Q3, answersheet=answersheet)
            if answer.answer != marital_status:
                Child.objects.filter(responder=answersheet.responser).delete()
            answer.answer = marital_status
            answer.point = Q3.options.get(value=marital_status).point
        else:
            answer = Answer(question=Q3, answersheet=answersheet, answer=marital_status,
                            point=Q3.options.get(value=marital_status).point)
        answer.save()

        # Q4 save answer...
        number_of_child = request.POST.get('number_of_child', None)
        if number_of_child is not None:
            if Answer.objects.filter(question=Q4, answersheet=answersheet).exists():
                answer = Answer.objects.get(question=Q4, answersheet=answersheet)
                Child.objects.filter(responder=answersheet.responser).delete()
                answer.answer = int(number_of_child)
                answer.point = 0
            else:
                answer = Answer(question=Q4, answersheet=answersheet, answer=int(number_of_child), point=0)
            answer.save()

        # T1 save answer...
        home = request.POST.get('home')
        if Answer.objects.filter(question=T1, answersheet=answersheet).exists():
            answer = Answer.objects.get(question=T1, answersheet=answersheet)
            answer.answer = home
            answer.point = T1.options.get(value=home).point
        else:
            answer = Answer(question=T1, answersheet=answersheet, answer=home,
                            point=T1.options.get(value=home).point)
        answer.save()

        # T2 save answer...
        job = request.POST.get('job')
        if Answer.objects.filter(question=T2, answersheet=answersheet).exists():
            answer = Answer.objects.get(question=T2, answersheet=answersheet)
            answer.answer = job
            answer.point = T2.options.get(value=job).point
        else:
            answer = Answer(question=T2, answersheet=answersheet, answer=job,
                            point=T2.options.get(value=job).point)
        answer.save()

        # T3 save answer...
        region = request.POST.get('region')
        if Answer.objects.filter(question=T3, answersheet=answersheet).exists():
            answer = Answer.objects.get(question=T3, answersheet=answersheet)
            answer.answer = region
            answer.point = T3.regions.get(value=region, city=answersheet.responser.city).point
        else:
            answer = Answer(question=T3, answersheet=answersheet, answer=region,
                            point=T3.regions.get(value=region, city=answersheet.responser.city).point)
        answer.save()

        # T4_1 save answer...
        if number_of_child is not None:
            if int(number_of_child) in [1, 2, 3]:
                first_child_year = int(request.POST.get('first_child_year'))
                first_child_gender = request.POST.get('first_child_gender')
                first_child_age = int(request.POST.get('first_child_age'))
                child = Child(responder=answersheet.responser, gender=first_child_gender,
                              birthday_year=first_child_year,
                              age=first_child_age)
                child.save()

            if int(number_of_child) in [2, 3]:
                second_child_year = int(request.POST.get('second_child_year'))
                second_child_gender = request.POST.get('second_child_gender')
                second_child_age = int(request.POST.get('second_child_age'))
                child = Child(responder=answersheet.responser, gender=second_child_gender,
                              birthday_year=second_child_year,
                              age=second_child_age)
                child.save()
            if int(number_of_child) >= 3:
                third_child_year = int(request.POST.get('third_child_year'))
                third_child_gender = request.POST.get('third_child_gender')
                third_child_age = int(request.POST.get('third_child_age'))
                child = Child(responder=answersheet.responser, gender=third_child_gender,
                              birthday_year=third_child_year,
                              age=third_child_age)
                child.save()

        answersheet.calculate_total_point()
        print('')
