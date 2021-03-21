from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
# Create your models here.
class UserInfo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ip_address = models.CharField(max_length=220, blank=True, null=True)
	last_login = models.DateTimeField(default=timezone.now)

	def __str__(self):
		text = f"User: {self.user}"
		return text