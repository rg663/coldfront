from coldfront.core.project.models import Project
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, generics
from django.views.generic.base import TemplateView
from rest_framework.renderers import JSONRenderer
from django.conf import settings

from coldfront.core.resource.models import ResourceAttribute, Resource
from coldfront.core.allocation.models import AllocationUser, Allocation

from coldfront.core.utils.common import import_from_settings
from coldfront.plugins.slurm.associations import SlurmCluster
from coldfront.plugins.slurm.utils import (SLURM_ACCOUNT_ATTRIBUTE_NAME,
                                           SLURM_CLUSTER_ATTRIBUTE_NAME,
                                           SLURM_USER_SPECS_ATTRIBUTE_NAME,
                                           SlurmError, slurm_remove_qos,
                                           slurm_dump_cluster, slurm_remove_account,
                                           slurm_remove_assoc)



from django.contrib.auth.models import User

# from coldfront.icm.account_applications.models import AccountApplication, AccountApplicationsGIDChoice, AccountApplicationsStatusChoice
from django.shortcuts import get_object_or_404#, render


from django_auth_ldap.backend import LDAPBackend
from coldfront.plugins.ldap_user_search.utils import LDAPUserSearch
import datetime
from django.db.models.query_utils import Q

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions

class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = ['id', 'all_public_attributes_as_list', 'project_id', 'resource']

    resource = serializers.SerializerMethodField()

    def get_resource(self, obj):
        return obj.resources.first().name

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']

    # resource = serializers.SerializerMethodField()

    # def get_resource(self, obj):
    #     return  obj.resources.first().name

class SLURMAccountsAPI(APIView):
    def get(self, request, cluster):
        #resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource
        resource = get_object_or_404(Resource,name=cluster)
        allocations= Allocation.objects.filter(
                resources=resource.pk, 
                status__name='Active', 
                allocationuser__user__pk=request.user.pk
        )
        return Response(AllocationSerializer(allocations, many=True).data)

class SLURMAccountsPublicAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #this is public api

    def get(self, request, username):
        #resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource

        allocations = Allocation.objects.filter(
                resources__in=Resource.objects.filter(is_public=True, resource_type__name__in=['Cluster','Cluster Partition']), 
                status__name='Active', 
                allocationuser__user__username=username
        ).distinct()
        return Response(AllocationSerializer(allocations, many=True).data)

class SLURMAccountsPublicAPIByAllocationStatus(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #this is public api

    def get(self, request, username, status):
        #resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource

        allocations = Allocation.objects.filter(
                resources__in=Resource.objects.filter(is_public=True, resource_type__name__in=['Cluster','Cluster Partition']), 
                status__name=status, 
                allocationuser__user__username=username
        ).distinct()
        print(request.user)
        return Response(AllocationSerializer(allocations, many=True).data)

class ProjectAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # def get_default_renderer(self, view):
    #     return JSONRenderer()
    # queryset = Project.objects.filter(
            # id=id, 
            # projectuser__user__username=request.user.username,
    # ).distinct()
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        project = Project.objects.filter(
                id=self.kwargs.get('id'), 
                # projectuser__user__username=request.user.username,
        ).distinct()
        return project

    def retrieve(self, request, *args, **kwargs):
        # pk = self.kwargs.get('id')
        # print(kwargs['id'])
        object = Project.objects.filter(id=kwargs['id'],projectuser__user__username=request.user.username).distinct()
        if object:
            serializer = ProjectSerializer(object, many=True)
            print(f"if! {serializer}")
            print(serializer.data)
        else:
            # serializer = ProjectSerializer()
            # print(f"else! {serializer}")
            return Response()
        return Response(serializer.data)

    # def get(self, request, id, format=None):
        # resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource
        # project = get_object_or_404(Project,id=id)
        # print("\n\n")
        # print(id)
        # print(request.user.username)

        # print("\n")
        # print(project)
        # return Response(ProjectSerializer(project, many=True).data)

@login_required
def show_auth_code(request):

    context = {
        'code': request.GET.get('code'),
    }

    return render(request, "show_code.html", context)

