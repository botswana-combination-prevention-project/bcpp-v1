from bhp_base_model.classes import BaseModelAdmin


class BaseCommentAdmin(BaseModelAdmin):

    list_display = ('created', 'subject', 'rt', 'status', 'user_created', 'user_modified', 'modified')
    search_fields = ('subject', 'comment', 'rt')
    list_filter = ('status', 'created', 'user_created', 'user_modified', 'modified')
