from django.contrib import admin
from .models import Ground, Image, Comment, Changes


admin.site.register(Ground)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Changes)
