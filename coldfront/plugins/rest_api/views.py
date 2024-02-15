from coldfront.core.field_of_science.models import FieldOfScience
from coldfront.core.project.models import Project, ProjectStatusChoice
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, generics
from rest_framework.reverse import reverse
from django.views.generic.base import TemplateView
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
    BasicAuthentication,
)
from django.conf import settings

from coldfront.core.resource.models import ResourceAttribute, Resource
from coldfront.core.allocation.models import AllocationUser, Allocation

from coldfront.core.utils.common import import_from_settings
from coldfront.plugins.slurm.associations import SlurmCluster
from coldfront.plugins.slurm.utils import (
    SLURM_ACCOUNT_ATTRIBUTE_NAME,
    SLURM_CLUSTER_ATTRIBUTE_NAME,
    SLURM_USER_SPECS_ATTRIBUTE_NAME,
    SlurmError,
    slurm_remove_qos,
    slurm_dump_cluster,
    slurm_remove_account,
    slurm_remove_assoc,
)


from django.contrib.auth.models import User

# from coldfront.icm.account_applications.models import AccountApplication, AccountApplicationsGIDChoice, AccountApplicationsStatusChoice
from django.shortcuts import get_object_or_404  # , render


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
        fields = ["id", "all_public_attributes_as_list", "project_id", "resource"]

    resource = serializers.SerializerMethodField()

    def get_resource(self, obj):
        return obj.resources.first().name

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class FoSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfScience
        fields = ["description"]

class ProjectStatusChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatusChoice
        fields = ["name"]

class ProjectSerializer(serializers.ModelSerializer):
    # pi = UserModelSerializer(read_only=True)
    # status = ProjectStatusChoiceSerializer(read_only=True)
    # field_of_science = FoSModelSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

class SLURMAccountsAPI(APIView):
    def get(self, request, cluster):
        # resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource
        resource = get_object_or_404(Resource, name=cluster)
        allocations = Allocation.objects.filter(
            resources=resource.pk,
            status__name="Active",
            allocationuser__user__pk=request.user.pk,
        )
        return Response(AllocationSerializer(allocations, many=True).data)


class SLURMAccountsPublicAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # this is public api

    def get(self, request, username):
        # resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource

        allocations = Allocation.objects.filter(
            resources__in=Resource.objects.filter(
                is_public=True, resource_type__name__in=["Cluster", "Cluster Partition"]
            ),
            status__name="Active",
            allocationuser__user__username=username,
        ).distinct()
        return Response(AllocationSerializer(allocations, many=True).data)


class SLURMAccountsPublicAPIByAllocationStatus(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # this is public api

    def get(self, request, username, status):
        # resource = ResourceAttribute.objects.get(resource_attribute_type_id=15, value=cluster).resource

        allocations = Allocation.objects.filter(
            resources__in=Resource.objects.filter(
                is_public=True, resource_type__name__in=["Cluster", "Cluster Partition"]
            ),
            status__name=status,
            allocationuser__user__username=username,
        ).distinct()
        print(request.user)
        return Response(AllocationSerializer(allocations, many=True).data)

class ProjectAPI(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    lookup_field = "id"

    def get_queryset(self):
        # if self.request.user.userprofile.is_pi:
        #     print("pi queryset")
        #     print(self.request.user.username)
        #     project = Project.objects.filter(
        #         id=self.kwargs.get("id"), pi__username=self.request.user.username
        #     )
        # else:
        print("non pi queryset")
        project = Project.objects.filter(
            id=self.kwargs.get("id"),
            projectuser__user__username=self.request.user.username,
        )
        # project = Project.objects.filter(
        #     pk=self.kwargs.get("id"),
        #     projectuser__user__username=self.request.user.username
        # )
        return project

    def retrieve(self, request, *args, **kwargs):
        object = Project.objects.filter(
            id=kwargs["id"], projectuser__user__username=request.user.username
        ).distinct()
        if object:
            serializer = ProjectSerializer(object, many=True)
            response = Response(serializer.data)
            print(f"if! {serializer}")
            print(serializer.data)
        else:
            response = Response()
        return response
    
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def perform_update(self, serializer):
    #     serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(type(instance))
        # serializer = self.get_serializer(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        # instance.projectstatuschoice_set.all().delete()
        instance.projectuser_set.all().delete()

        instance.projectreview_set.all().delete()
        instance.projectadmincomment_set.all().delete()
        instance.projectuser_set.all().delete()

        instance.delete()

class ProjectListAPI(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    lookup_field = "id"

    def get_queryset(self):
        
        if self.request.user.userprofile.is_pi:
            project = Project.objects.filter(pi__username=self.request.user.username)
        else:
            project = Project.objects.filter(
                projectuser__user__username=self.request.user.username
            )
        return project


@login_required
def show_auth_code(request):
    context = {
        "code": request.GET.get("code"),
    }

    return render(request, "show_code.html", context)
