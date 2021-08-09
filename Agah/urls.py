from django.urls import path

from Agah import views

urlpatterns = [
    path('survey/<int:pk>', views.Survey_View.as_view(), name='survey'),
    path('personal/<int:pk>', views.Personal, name='persnoal'),
    path('social/', views.Social, name='social'),
    path('interviwer_name/', views.interviwer_name, name='interviwer_name'),
]
