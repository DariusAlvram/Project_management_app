from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile

class dashboardView(View):
    def get(self, request, *args, **kwargs):
        lastest_projects = Project.objects.all()[:5]
        lastest_tasks = Task.objects.all()[:5]
        latest_members = Profile.objects.all()[:8] 
        context = {}
        context["lastest_projects"] = lastest_projects
        context["lastest_tasks"] = lastest_tasks
        context["latest_members"] = latest_members
        return render(request, 'accounts/dashboard.html', context)
