from django.urls import path

from . import views

app_name = "customreportapp"
urlpatterns = [
    # path("<int:model_field1>/", views.detail, name="detail"),
    # path("<int:model_field2>/results/", views.results, name="results"),
    path("", views.index, name="custom-report"),
]