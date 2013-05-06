from bhp_base_model.classes import BaseModelAdmin


class BaseCommentAdmin(BaseModelAdmin):

    def __init__(self, *args, **kwargs):
        super(BaseCommentAdmin, self).__init__(*args, **kwargs)
        self.search_fields = ['subject', 'comment', 'rt']
        self.list_display = ['created', 'subject', 'rt', 'status', 'user_created', 'user_modified', 'modified']

    list_filter = ('status', 'created', 'user_created', 'user_modified', 'modified')
