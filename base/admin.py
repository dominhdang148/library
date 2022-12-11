from django.contrib import admin
from .models import Document, Topic, Comment
# Register your models here.

admin.site.register(Topic)
admin.site.register(Document)
admin.site.register(Comment)

