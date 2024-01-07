
from django.urls import include, path

from django.urls import path, include
from django.contrib.auth.models import User
# from coldfront.icm.account_applications.models import AccountApplication, AccountApplicationsStatusChoice
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views
from coldfront.plugins.rest_api.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import generics


urlpatterns = [
    path('allocations/slurm/<str:cluster>/', SLURMAccountsAPI.as_view(), name='user-slurm-accounts'),
    # path('public/allocations/slurm/<str:username>/', SLURMAccountsPublicAPI.as_view(), name='user-slurm-accounts-public'),
    # path('public/allocations/slurm/<str:username>/status/<str:status>/', SLURMAccountsPublicAPIByAllocationStatus.as_view(), name='user-slurm-accounts-public-status'),
    path('o/showcode', show_auth_code, name='show-auth-code'),

    path('projects/<int:id>/', ProjectAPI.as_view(), name='project-via-id'),
    path('projects/', ProjectListAPI.as_view(), name='project-list-api')
]

urlpatterns = format_suffix_patterns(urlpatterns)