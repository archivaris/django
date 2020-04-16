# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import StudentForm
from .models import Student


@login_required
def add_student_view(request):
    """
    :param request:
    :return: admission form to
    logged in user.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            pk = form.instance.pk
            return redirect('students:student_details', pk=pk)
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'students/addstudent.html', context)


@login_required
def students_view(request):
    """
    :param request:
    :return: renders student list with all department
    and semesters list.
    """
    all_students = Student.objects.select_related(
        'department', 'semester', 'ac_session').all()

    context = {'students': all_students,
               }
    return render(request, 'students/students_list.html', context)
