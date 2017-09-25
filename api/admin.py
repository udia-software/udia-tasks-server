from django.contrib import admin
from api.models import Goal, Task, TaskAction

# Register your models here.
admin.site.register(Goal)
admin.site.register(Task)
admin.site.register(TaskAction)
