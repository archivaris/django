from django.urls import path, re_path

from . import views

urlpatterns = [
    path('students/', views.students_view, name='students'),
    path('students/add/', views.user_add, name='user_add'),

    path('profile/<int:pk>', views.student_detail, name='student_detail'),
    path('profile/edit/<int:pk>', views.user_edit, name='user_edit'),
    path('user/delete/<int:pk>', views.user_delete, name='user_delete'),

    path('permits/', views.permits_view, name='permits'),
    path('permits/add/', views.permit_add, name='permit_add'),
    path('permits/edit/<int:pk>', views.permit_edit, name='permit_edit'),
    path('permits/delete/<int:pk>', views.permit_delete, name='permit_delete'),
    path('permits/<int:pk>/course/add/', views.course_add, name='course_add'),
    path('permits/<int:p_pk>/course/delete/<int:pk>', views.course_delete, name='course_delete'),
    path('permits/course/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('permits/course/<int:pk>', views.course_detail, name='course_detail'),
    path('permit/<int:pk>', views.permit_detail, name='permit_single'),

    path('course/<int:course_id>/instructor/edit/', views.select_instructor, name='add_instructor'),
    path('course/<int:course_id>/instructor/confirm/<int:student_id>', views.confirm_select_instructor, name='confirm_instructor'),
    path('course/<int:course_id>/instructor/delete/<int:student_id>', views.confirm_delete_instructor, name='delete_instructor'),

    path('ajax/filter_course/', views.filter_courses_view, name='filter_views'),

    re_path(r'^$', views.home_view, name='home'),

    path('payment/all/', views.payment_deadlines, name='payment'),
    path('payment/current/', views.done_payments, name='current_payments'),
    path('administrator/<int:extra_time>', views.admin_view, name='administrator'),
    path('deadline/delete/<int:pk>', views.delete_payment, name='delete_payment'),

]
