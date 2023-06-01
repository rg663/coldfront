from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, Http404

# def index(request):
#     return HttpResponse("Hello, world. You're at the home index.")

from .models import Allocation

from django.template import loader

def index(request):
    project_list = Allocation.objects.order_by("-end_date")
    context = {"projects": project_list}
    return render(request, "index.html", context)

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