from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User

# Possible values for status field
status_choices = [
    ('To Do', 'To Do'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
]

# Possible values for priority field
priority_choices = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
]

# Project Fields defintion and possible values
class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255) 
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='To Do')
    priority = models.CharField(max_length=20, choices=priority_choices, default='Medium')
    start_date = models.DateField()
    due_date = models.DateField()
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_on']
        
    # Calculation remaining days to compelete project  
    def days_until_due(self):
        if self.due_date:
            # Get current date
            current_date = timezone.now().date()
            # Calculate the difference in days
            number_days = (self.due_date - current_date).days
            #Generate string for days remaining
            if number_days == 1 :
                return str(number_days) + " day"
            elif number_days == -1:
                return str(number_days) + " day"
            else:
                return str(number_days) + " days"
            
        return None

# Logic for set progress percentage for project in Dashboard
    @property
    def progress(self):
        progress_dic = {
            'To Do': 0,
            'In Progress': 50,
            'Completed': 100,
        }
        return progress_dic.get(self.status, 0)
    
# Color for progress bar in Dashboard
    @property
    def status_color(self):
        status_value = self.progress
        if status_value == 100:
            color = 'success'
        elif status_value == 50:
            color = 'primary'
        else:
            color = ''
            
        return color
    
    # Color code for status in Dashboard
    def priority_color(self):
        if self.priority == 'Low':
            color = 'success'
        elif self.priority == 'Medium':
            color =  'warning'
        else:
            color = 'danger'
        return color