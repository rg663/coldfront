from django.db import models

# Create your models here.
# from django.utils import timezone

from coldfront.core.allocation.models import *
from coldfront.core.project.models import *
from coldfront.core.resource.models import *
from coldfront.core.user.models import *

# class TestModel(models.Model):
#     model_field1 = models.CharField(max_length=200)
#     model_field2 = models.DateTimeField("Time Here")

#     def __str__(self):
#         return self.model_field1

#     # def __str__(self):
#     #     return self.model_field1

#     # def was_published_recently(self):
#     #     return self.model_field2 >= timezone.now()

# class TestModel2(models.Model):
#     model_above = models.ForeignKey(TestModel, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     model_field3 = models.IntegerField(default=0)

#     # def __str__(self) -> str:
#     #     return super().__str__()

#     def __str__(self):
#         return self.choice_text