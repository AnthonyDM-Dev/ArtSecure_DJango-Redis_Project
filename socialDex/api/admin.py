from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
	fieldsets = ('User data', {'fields': ['user', 'address']}),\
				('Transaction info', {'fields': ['title', 'composition', 'txId', 'hash', 'datetime']})

# Register your models here.
admin.site.register(Post, PostAdmin)