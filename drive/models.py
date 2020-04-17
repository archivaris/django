from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

STATUS = (
    (0, 'Processing'),
    (1, 'Approved'),
    (2, 'Refused'),
)

DAYS = (
    [(i, i) for i in range(1, 31)]
)

MONTHS = (
    (1, 'Jan'),
    (2, 'Feb'),
    (3, 'Mar'),
    (4, 'Apr'),
    (5, 'May'),
    (6, 'Jun'),
    (7, 'Jul'),
    (8, 'Aug'),
    (9, 'Sep'),
    (10, 'Oct'),
    (11, 'Nov'),
    (12, 'Dec'),
)

TYPES = (
    ('o', 'Mandatory'),
    ('z', 'Optional'),
)


class Permit(models.Model):
    name = models.CharField(max_length=150)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField(max_length=600, null=True, blank=True)
    permit = models.ForeignKey(Permit, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.IntegerField(null=True, default=0)
    obligative = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_type(self):
        if self.obligative:
            return "O"
        else:
            return "Z"


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    permit = models.ForeignKey(Permit, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100, null=True)
    course = models.ManyToManyField(Course, related_name='course', blank=True)
    course_instructor = models.ManyToManyField(Course, related_name='course_teacher', blank=True)

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Student'


def create_profile(sender, **kwargs):
    if kwargs['created']:
        student = Student.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.student.student.first_name + ' ' + self.student.student.last_name


def get_full_name(self):
    if self.student.first_name and self.student.last_name:
        return self.student.first_name + ' ' + self.student.last_name
    return self.username


User.add_to_class("__str__", get_full_name)


class payment_deadlines(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name
        return "Deadline (" + str(self.pk) + ")"


class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    deadline = models.ForeignKey(payment_deadlines, on_delete=models.CASCADE, null=True)
    refused = models.BooleanField(default=False)

    def __str__(self):
        if self.student.student.first_name and not self.student.student.last_name:
            return self.student.student.first_name + ' - ' + self.deadline.name + ' - ' + self.course.name
        elif self.student.student.first_name and self.student.student.last_name:
            return self.student.student.first_name + ' ' + self.student.student.last_name + ' - ' + self.deadline.name + ' - ' + self.course.name
        else:
            return 'Student' + ' - ' + self.deadline.name
