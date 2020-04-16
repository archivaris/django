from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
    path('all/', views.students_view, name='all_student'),
    path('add/', views.add_student_view, name='add_student'),
]
