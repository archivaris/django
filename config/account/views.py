from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView
from students.models import Student

from .forms import UserRegistrationForm


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    context = {
        'total_students': total_students,
    }
    return render(request, 'dashboard.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            auth_user = authenticate(username=user_form.cleaned_data['username'],
                                     password=user_form.cleaned_data['password'])
            if auth_user is not None:
                login(request, auth_user)
            return redirect('account:dashboard')
        else:
            return render(request, 'account/register.html', {'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


class AccountListView(ListView):
    model = User
    template_name = 'admin_tools/accounts_list.html'
    context_object_name = 'accounts'
