from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile
from notifications.models import Notification

class dashboardView(View):
    def get(self, request, *args, **kwargs):
        lastest_projects = Project.objects.all()[:5]
        lastest_tasks = Task.objects.all()[:5]
        latest_members = Profile.objects.all()[:8] 
        latest_notifications = Notification.objects.for_user(request.user).filter(read=False)
        context = {}
        context["lastest_projects"] = lastest_projects
        context["lastest_tasks"] = lastest_tasks
        context["latest_members"] = latest_members
        context["latest_notifications"] = latest_notifications[:3]
        context["notifications_count"] = latest_notifications.filter(read=False).count()
        return render(request, 'accounts/dashboard.html', context)
