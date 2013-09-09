from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

register = template.Library()


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def bhp_submit_row(context):
    try:
        ctx = original_submit_row(context)
    except KeyError:
        ctx = {'add': True}
    is_popup = context.get('is_popup', False)
    request = context.get('request', None)
    show = request.GET.get('show') == 'forms'
    ctx.update({
        #'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        #'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
        'show_savenext': (not is_popup and context.get('add') and show)
        })
    return ctx


# @register.inclusion_tag('admin/submit_line.html', takes_context=True)
# def bhp_submit_row(context):
#     """
#     Displays the row of buttons for delete and save.
#     """
#     opts = context['opts']
#     change = context['change']
#     is_popup = context['is_popup']
#     save_as = context['save_as']
#     return {
#         'onclick_attrib': (opts.get_ordered_objects() and change
#                             and 'onclick="submitOrderForm();"' or ''),
#         'show_delete_link': (not is_popup and context['has_delete_permission']
#                               and (change or context['show_delete'])),
#         'show_save_as_new': not is_popup and change and save_as,
#         'show_save_and_add_another': context['has_add_permission'] and
#                             not is_popup and (not save_as or context['add']),
#         'show_save_and_continue': not is_popup and context['has_change_permission'],
#         'is_popup': is_popup,
#         'show_save': True,
#         'show_savenext': (not is_popup and context['add'])
#     }
