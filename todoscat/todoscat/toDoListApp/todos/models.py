from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class todo_grup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grup_name = models.CharField(max_length=1000)

    
    
    def __str__(self):
        return self.grup_name

class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grup = models.ForeignKey(todo_grup, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=None, null=True)
    description = models.CharField(max_length=1000)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.todo_name