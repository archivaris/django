from django.contrib import admin

from .models import Course, Permit, State, Student, Grade, payment_deadlines, Payment


class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade',)


admin.site.register(Payment)
admin.site.register(payment_deadlines)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Permit)
admin.site.register(State)
