from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):        
	name=models.CharField(max_length=20, null=False, blank=False, unique=True)
	def __str__(self):
		return self.nome

