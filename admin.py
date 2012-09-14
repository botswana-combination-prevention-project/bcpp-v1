from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from models import Comment


class CommentAdmin(BaseModelAdmin):

    list_display = ('created', 'subject', 'rt', 'status', 'user_created', 'user_modified', 'modified')
    search_fields = ('subject', 'comment', 'rt')
    list_filter = ('status', 'created', 'user_created', 'user_modified', 'modified')

admin.site.register(Comment, CommentAdmin)
