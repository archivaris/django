from django.urls import path, re_path

from . import views

urlpatterns = [
    path('students/', views.students_view, name='students'),
    path('students/add/', views.user_add, name='user_add'),
    path('profile/<int:pk>', views.student_detail, name='student_detail'),
    path('profile/edit/<int:pk>', views.user_edit, name='user_edit'),
    path('user/delete/<int:pk>', views.user_delete, name='user_delete'),
    path('programs/', views.programs_view, name='programs'),
    path('programs/add/', views.program_add, name='program_add'),
    path('programs/edit/<int:pk>', views.program_edit, name='program_edit'),
    path('programs/delete/<int:pk>', views.program_delete, name='program_delete'),
    path('programs/<int:pk>/course/add/', views.course_add, name='course_add'),
    path('programs/<int:p_pk>/course/delete/<int:pk>', views.course_delete, name='course_delete'),
    path('programs/course/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('programs/course/<int:pk>', views.course_detail, name='course_detail'),
    path('program/<int:pk>', views.program_detail, name='program_single'),
    path('course/<int:course_id>/teacher/edit/', views.select_teacher, name='add_teacher'),
    path('course/<int:course_id>/teacher/confirm/<int:student_id>', views.confirm_select_teacher,
         name='confirm_teacher'),
    path('course/<int:course_id>/teacher/delete/<int:student_id>', views.confirm_delete_teacher, name='delete_teacher'),
    path('ajax/filter_course/', views.filter_courses_view, name='filter_views'),
    re_path(r'^$', views.home_view, name='home'),
    path('provimet/paraqitura/', views.provimet_paraqitura, name='provimet_paraqitura'),
    path('administrator/<int:afat_extra>', views.admin_view, name='administrator'),
    path('afati/delete/<int:pk>', views.delete_afat, name='delete_afat'),

    # remove
    # path('provimet/paraqit/', views.paraqit_provimet, name='provimet'),
    # path('provimet/paraqit/<int:c_pk>/<int:a_pk>', views.paraqit_provimin, name='paraqit_provimin'),
    # path('course/<int:course_id>/grades/', views.grade_students, name='grade_students'),
    #
]
