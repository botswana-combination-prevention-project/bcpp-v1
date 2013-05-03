from django.contrib import admin
from bhp_data_manager.models import Comment
from base_comment_admin import BaseCommentAdmin


class CommentAdmin(BaseCommentAdmin):
        pass
admin.site.register(Comment, CommentAdmin)
