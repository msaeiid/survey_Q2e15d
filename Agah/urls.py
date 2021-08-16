from django.urls import path

from Agah import views

app_name = 'agah'

urlpatterns = [
    path('survey/<int:pk>', views.Survey_View.as_view(), name='survey'),
    path('personal/<int:pk>', views.Personal, name='persnoal'),
    path('social/', views.Social, name='social'),
    path('interviwer_name/', views.interviwer_name, name='interviwer_name'),
    path('brand/', views.Brand, name='brand'),
    path('sentecnce/', views.Sentence, name='sentence')
]
