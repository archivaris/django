import debug_toolbar
from account.views import dashboard
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "SMS-LIO Admin"
admin.site.site_title = "SMS-LIO Admin Portal"
admin.site.index_title = "Welcome to SMS-LIO Portal"

urlpatterns = [
    path('__debug__', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', dashboard, name='index_view'),
    path('account/', include('account.urls')),
    path('students/', include('students.urls')),
]
