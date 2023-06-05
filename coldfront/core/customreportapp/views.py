from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, Http404
from django.db.models import Q

# def index(request):
#     return HttpResponse("Hello, world. You're at the home index.")

from .models import *

from django.template import loader

def index(request):
    context = {}
    template_name = 'index.html'
    if request.user.is_authenticated:
        project_list = Project.objects.filter(
            (Q(pi=request.user) & Q(status__name__in=['New', 'Active', ])) |
            (Q(status__name__in=['New', 'Active', ]) &
             Q(projectuser__user=request.user) &
             Q(projectuser__status__name__in=['Active', ]))
        ).distinct().order_by('-created')

        allocation_list = Allocation.objects.filter(
            Q(status__name__in=['Active', 'New', 'Renewal Requested', ]) &
            Q(project__status__name__in=['Active', 'New']) &
            Q(project__projectuser__user=request.user) &
            Q(project__projectuser__status__name__in=['Active', ]) &
            Q(allocationuser__user=request.user) &
            Q(allocationuser__status__name__in=['Active', ])
        ).distinct().order_by('-created')

        resource_list = Resource.objects.distinct()
        user_list = User.objects.distinct()
        context['project_list'] = project_list
        context['allocation_list'] = allocation_list
        context['new_allocations'] = [allocation for allocation in allocation_list if allocation.start_date != None and datetime.today().date() - allocation.start_date <= timedelta(days=7)]
        context['allocations_expiring_soon'] = [allocation for allocation in allocation_list if allocation.end_date != None and allocation.expires_in <= 30]
        context['resource_list'] = resource_list
        context['resource_types_initial'] = [res.resource_type for res in resource_list]
        context['resource_types_in_between'] = {}
        for res_type in context['resource_types_initial']:
            context['resource_types_in_between'][res_type] = 0
        for res in context['resource_types_initial']:
            context['resource_types_in_between'][res] += 1
        context['resource_types'] = []
        for res_type, count in context['resource_types_in_between'].items():
            new_list = [res_type.name, count]
            context['resource_types'].append(new_list)
        context['user_list'] = user_list
        context['users_from_this_week'] = [user for user in user_list if user.last_login != None and datetime.today().date() - user.last_login.date() <= timedelta(days=7)]
        context['all_other_users'] = [user for user in user_list if user not in context['users_from_this_week']]
        # try:
        #     context['ondemand_url'] = settings.ONDEMAND_URL
        # except AttributeError:
        #     pass

    # context['EXTRA_APPS'] = settings.INSTALLED_APPS

    # if 'coldfront.plugins.system_monitor' in settings.INSTALLED_APPS:
    #     from coldfront.plugins.system_monitor.utils import get_system_monitor_context
    #     context.update(get_system_monitor_context())

    return render(request, template_name, context)

    # project_list = Allocation.objects.order_by("-end_date")
    # context = {"projects": project_list}
    # return render(request, "index.html", context)

# class ProjectAttributeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = ProjectAttribute
#     form_class = ProjectAttributeAddForm
#     template_name = 'project/project_attribute_create.html'

#     def test_func(self):
#         """ UserPassesTestMixin Tests"""
#         project_obj = get_object_or_404(Project, pk=self.kwargs.get('pk'))

#         if self.request.user.is_superuser:
#             return True

#         if project_obj.pi == self.request.user:
#             return True

#         if project_obj.projectuser_set.filter(user=self.request.user, role__name='Manager', status__name='Active').exists():
#             return True

#         messages.error(
#             self.request, 'You do not have permission to add project attributes.')

#     def get_initial(self):
#         initial = super().get_initial()
#         pk = self.kwargs.get('pk')
#         initial['project'] = get_object_or_404(Project, pk=pk)
#         initial['user'] = self.request.user
#         return initial

#     def get_form(self, form_class=None):
#         """Return an instance of the form to be used in this view."""
#         form = super().get_form(form_class)
#         form.fields['project'].widget = forms.HiddenInput()
#         return form

#     def get_context_data(self, *args, **kwargs):
#         pk = self.kwargs.get('pk')
#         context = super().get_context_data(*args, **kwargs)
#         context['project'] = get_object_or_404(Project, pk=pk)
#         return context

#     def get_success_url(self):
#         return reverse('project-detail', kwargs={'pk': self.object.project_id})


# def index(request):
#     latest_question_list = TestModel.objects.order_by("-model_field2")[:5]
#     output = ", ".join([q.model_field1 for q in latest_question_list])
#     return HttpResponse(output)


# Leave the rest of the views (detail, results, vote) unchanged

# def detail(request, model_field1):
#     question = get_object_or_404(TestModel, pk=model_field1)
#     return render(request, "detail.html", {"question": question})

# def results(request, model_field2):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % model_field2)