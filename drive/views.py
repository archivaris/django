from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Course, Permit, Student, Grade, payment_deadlines, Payment
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count
from .forms import UpdateProfile, CourseAddForm, PermitForm, DeadlinesForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django import forms
from django.template.defaulttags import register

max_counter = 3


@register.filter
def toInt(value):
    return int(value)


@register.filter
def toStr(value):
    return str(value)


@register.filter
def addOne(value):
    value = value + 1
    return value


@register.filter
def get_grade(course, user):
    grade = list(Grade.objects.values_list('grade', flat=True).filter(course__pk=course, student__pk=user))
    if not grade:
        return 0
    return grade[0]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def sub(value, arg):
    return value - arg


def permits_view(request):
    permits = Permit.objects.all()

    if request.user.is_authenticated:
        return render(
            request,
            'permits_list.html',
            {'permits': permits},
        )
    else:
        return redirect('login')


def permit_add(request):
    if request.method == 'POST':
        form = PermitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('permits')
    else:
        form = PermitForm()

    return render(
        request, 'permit_add.html', {'form': form},
    )


def permit_delete(request, pk):
    permit = Permit.objects.get(pk=pk)
    permit.delete()

    return redirect('permits')


def permit_edit(request, pk):
    permit = Permit.objects.get(pk=pk)

    if request.method == 'POST':
        form = PermitForm(request.POST, instance=permit)
        if form.is_valid():
            form.save()
            return redirect('permits')
    else:
        form = PermitForm(instance=permit)

    return render(
        request, 'program_add.html', {'form': form},
    )


def permit_detail(request, pk):
    permit = Permit.objects.get(pk=pk)
    courses = Course.objects.filter(permit_id=pk)

    paginator = Paginator(courses, 10)
    page = request.GET.get('page')

    courses = paginator.get_page(page)

    if request.user.is_authenticated:
        return render(
            request,
            'permit_single.html',
            {'permit': permit, 'courses': courses, 'credits': credits},
        )
    else:
        return redirect('login')


def students_view(request):
    students = Student.objects.all()
    permits = Permit.objects.all()

    if request.method == 'GET':
        p = request.GET.get('permit', '')
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')

        if p != '':
            students = Student.objects.filter(permit=p, first_name__contains=name, email__contains=email)
        else:
            students = Student.objects.filter(first_name__contains=name, email__contains=email)

    if request.user.is_authenticated:
        return render(
            request,
            'students_list.html',
            {'students': students, 'permits': permits},
        )
    else:
        return redirect('login')


def student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    success = Grade.objects.filter(student=student.user).order_by('-grade')
    details = Grade.objects.filter(student=student.user, grade__gt=4).aggregate(Avg('grade'), Max('grade'),
                                                                                Min('grade'))

    if request.user.is_authenticated:
        return render(
            request, 'student_profile.html', {'student': student, 'success': success, 'details': details},
        )
    else:
        return redirect('login')


def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    users = User.objects.filter(student__course_instructor__in=[course])
    grades = Grade.objects.filter(student_id=request.user.id, course_id=pk)
    instructors = Student.objects.filter(course_instructor__in=[course])

    if request.user.is_authenticated:
        return render(
            request, 'course_single.html',
            {'usrs': users, 'course': course, 'grades': grades, 'instructors': instructors},
        )
    else:
        return redirect('login')


def update_instructor(pk_t1):
    pk_t1 = int(pk_t1)
    if pk_t1 > 0:
        course = Course.objects.latest('pk')
        t1 = User.objects.get(pk=pk_t1)

        if not User.objects.filter(student__course_instructor__in=[course], pk=pk_t1).exists():
            t1.student.course_instructor.add(course)


def course_add(request, pk):
    users = User.objects.all()
    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        if form.is_valid():
            form.save()
            update_instructor(request.POST.get('user_1'))
            if request.POST.get('submit') != 'Save':
                return redirect('course_add', pk=pk)
            return redirect('permit_single', pk=request.POST.get('permit'))
    else:
        form = CourseAddForm(initial={'permit': Permit.objects.get(pk=pk)})

    if request.user.is_authenticated and request.user.is_superuser:
        return render(
            request, 'course_add.html', {'form': form, 'permit': pk, 'users': users},
        )
    else:
        return redirect('login')


def course_edit(request, pk):
    users = User.objects.all()
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseAddForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('permit_single', pk=request.POST.get('permit'))
    else:
        form = CourseAddForm(instance=course)

    # print(form.errors)

    if request.user.is_authenticated and request.user.is_superuser:
        return render(
            request, 'course_add.html', {'form': form, 'permit': pk, 'users': users, 'course': pk},
        )
    else:
        return redirect('login')


def course_delete(request, pk, p_pk):
    course = Course.objects.get(pk=pk)
    course.delete()

    return redirect('permit_single', pk=p_pk)


def user_add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uid = Student.objects.latest('pk').pk
            return redirect('user_edit', pk=uid)
    else:
        form = UserCreationForm()

    print(form.errors)

    if request.user.is_authenticated and request.user.is_superuser:
        return render(
            request, 'user_add.html', {'form': form},
        )
    else:
        return redirect('login')


def user_delete(request, pk):
    usr = get_object_or_404(User, pk=pk)
    usr.delete()

    return redirect('students')


def user_edit(request, pk):
    student = Student.objects.get(pk=pk)

    instance = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save(commit=False)

            courses = request.POST.getlist('course')

            is_super = request.POST.get('is_super')

            if is_super:
                usr = User.objects.get(pk=student.user.pk)
                usr.is_admin = True
                usr.is_staff = True
                usr.is_superuser = True
                usr.save()

            for c in courses:
                grade = Grade()
                usr = User.objects.get(pk=request.POST.get('user'))
                crs = Course.objects.get(pk=c)
                if not Grade.objects.filter(course=crs, student=usr).exists():
                    grade.student = usr
                    grade.grade = 0
                    grade.course = crs
                    grade.save()

            existing_courses = list(Student.objects.values_list('course', flat=True).filter(pk=pk))

            for c in existing_courses:
                if str(c) not in courses:
                    Grade.objects.filter(student=User.objects.get(pk=request.POST.get('user')), course=c).delete()

            form.save()
            return redirect('students')
    else:
        form = UpdateProfile(instance=instance,
                             initial=({'is_super': User.objects.get(pk=student.user.pk).is_superuser}))

    return render(
        request, 'user_profile_edit.html', {'form': form, 'student': student},
    )


def select_instructor(request, course_id):
    students = Student.objects.all()
    curr_instructor = Student.objects.filter(course_instructor__in=[Course.objects.get(pk=course_id)])

    if request.method == 'GET':
        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        students = Student.objects.filter(first_name__contains=first_name, last_name__contains=last_name).exclude(
            course_instructor__in=[Course.objects.get(pk=course_id)])

    paginator = Paginator(students, 15)

    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render(
        request, 'select_instructor.html',
        {'students': students, 'course_id': course_id, 'instructors': curr_instructor},
    )


def confirm_select_instructor(request, course_id, student_id):
    student = Student.objects.get(pk=student_id)
    course = Course.objects.get(pk=course_id)

    student.course_instructor.add(course)
    student.save()

    return redirect('add_instructor', course_id=course_id)


def confirm_delete_instructor(request, course_id, student_id):
    student = Student.objects.get(pk=student_id)
    course = Course.objects.get(pk=course_id)

    student.course_instructor.remove(course)
    student.save()

    return redirect('add_instructor', course_id=course_id)


# AJAX Call
def filter_courses_view(request):
    program = request.GET.get('program', None)
    course = Course.objects.filter(program=program).values('pk', 'name', 'obligative', )
    data = list(course)
    return JsonResponse(data, safe=False)


def home_view(request):
    permits = Permit.objects.all()
    users = User.objects.all().order_by('-last_login')[:5]

    if request.user.is_authenticated:
        return render(
            request, 'home.html', {'permits': permits, 'users': users},
        )
    else:
        return redirect('login')


# ADMIN
def admin_view(request, extra_time):
    if not extra_time:
        extra_time = 0

    queryset = payment_deadlines.objects.all()
    DeadlinesFormSet = forms.modelformset_factory(payment_deadlines, form=DeadlinesForm, extra=extra_time)

    if request.method == 'POST':
        formset = DeadlinesFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            for instance in formset.forms:
                if instance.cleaned_data.get('name'):
                    instance.save()
            return redirect('administrator', extra_time=0)
        else:
            print(formset.errors)
    else:
        formset = DeadlinesFormSet(queryset=queryset)

    return render(
        request, 'admin_panel.html', {'formset': formset, 'extra': extra_time},
    )


def delete_payment(request, pk):
    deadline = get_object_or_404(payment_deadlines, pk=pk)
    deadline.delete()

    return redirect('administrator', afat_extra=0)


def current_payments(request):
    paymentList = list()
    courses = None
    payment = None
    deadline = payment_deadlines.objects.filter(aktiv=True)
    deadlineAll = payment_deadlines.objects.all()
    permit = request.user.student.permit

    if request.method == 'GET':
        if request.GET.get('filter'):

            if int(request.GET.get('deadline')) > -1:
                deadline = get_object_or_404(payment_deadlines, pk=int(request.GET.get('deadline')))
                paymentList = list(
                    Payment.objects.values_list('course', flat=True).filter(student=request.user, deadline=deadline))

            courses = Course.objects.filter(permit=permit).exclude(
                pk__in=paymentList).annotate(hera=Count('pk'))

    return render(
        request, 'paraqit_provimet.html',
        {'permit': permit, 'courses': courses, 'payment': payment, 'deadline': deadline, 'deadlineAll': deadlineAll},
    )


def done_payments(request):
    deadlineAll = payment_deadlines.objects.all()
    permit = request.user.student.permit
    payment = None;

    if request.method == 'GET':
        if request.GET.get('filterPayment'):
            if int(request.GET.get('deadline')) >= 0:
                payment = Payment.objects.filter(student=request.user, deadline=int(request.GET.get('deadline')))
    return render(
        request, 'done_payments.html', {'permit': permit, 'payment': payment, 'deadlineAll': deadlineAll},
    )


def now_payment(request, c_pk, a_pk):
    course = Course.objects.get(pk=c_pk)
    payment = Payment()
    payment.course = course
    payment.student = request.user
    payment.deadline = payment_deadlines.objects.get(pk=a_pk)
    payment.time = datetime.now()
    payment.refuzuar = False
    payment.save()

    return redirect('payment')
