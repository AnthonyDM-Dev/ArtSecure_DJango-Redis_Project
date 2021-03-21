from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from api.utils import sendTransaction
from api import wallet
import hashlib

User = get_user_model()
# Create your models here.
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField('Date published', default=timezone.now)
	title = models.CharField(max_length=120, default=None)
	composition = models.TextField()
	address = models.CharField(max_length=66, default=None, null=True)
	hash = models.CharField(max_length=32, default=None, null=True)
	txId = models.CharField(max_length=66, default=None, null=True)

	def __str__(self):
		text = f'New post from {self.user}. Date published: {self.datetime}'
		return text

	def writeOnChain(self):
		content = f"Title: {self.title}\nComposition: {self.composition}"
		self.address = wallet.address
		self.hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
		self.txId = sendTransaction(self.hash)
		self.save()