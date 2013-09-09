from django.contrib import messages
from bhp_sync.classes import SerializeToTransaction
from bhp_crypto.classes import FieldCryptor


def serialize(modeladmin, request, queryset):

    """ for a model instance serializing to outgoing"""
    serialize_to_transaction = SerializeToTransaction()
    n = 0
    for instance in queryset:
        serialize_to_transaction.serialize(instance.__class__, instance)
        n += 1
    messages.add_message(request, messages.SUCCESS, '%s transactions have been sent to Outgoing' % (n,))
serialize.short_description = "Send as Outgoing Transaction"


def reset_transaction_as_not_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed = False"""
    for qs in queryset:
        qs.is_consumed = False
        qs.consumer = None
        qs.save()
reset_transaction_as_not_consumed.short_description = "Set transactions as NOT consumed (is_consumed=False)"

def reset_outgoing_transaction_server_as_not_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed_server = False"""
    for qs in queryset:
        qs.is_consumed_server = False
        qs.consumer = None
        qs.save()
reset_outgoing_transaction_server_as_not_consumed.short_description = "Set transactions as NOT consumed by Server(is_consumed_server=False)"

def reset_outgoing_transaction_server_as_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed_server = True"""
    for qs in queryset:
        qs.is_consumed_server = True
        qs.consumer = None
        qs.save()
reset_outgoing_transaction_server_as_consumed.short_description = "Set transactions as consumed by Server(is_consumed_server=True)"

def reset_outgoing_transaction_middle_as_not_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed_middleman = False"""
    for qs in queryset:
        qs.is_consumed_middleman = False
        qs.consumer = None
        qs.save()
reset_outgoing_transaction_middle_as_not_consumed.short_description = "Set transactions as NOT consumed by MiddleMan(is_consumed_middleman=False)"

def reset_outgoing_transaction_middle_as_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed_middleman = True"""
    for qs in queryset:
        qs.is_consumed_middleman = True
        qs.consumer = None
        qs.save()
reset_outgoing_transaction_middle_as_consumed.short_description = "Set transactions as consumed by MiddleMan(is_consumed_middleman=True)"

def reset_transaction_as_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_consumed = True"""
    for qs in queryset:
        qs.is_consumed = True
        qs.save()
reset_transaction_as_consumed.short_description = "Set transactions as consumed (is_consumed=True)"

def reset_transaction_as_ignored_and_consumed(modeladmin, request, queryset):
    """ reset transaction by setting is_ignored = True and is_consumed = True"""
    for qs in queryset:
        qs.is_consumed = True
        qs.is_ignored = True
        qs.save()
reset_transaction_as_ignored_and_consumed.short_description = "Set transactions as ignored and consumed (is_ignored=True, is_consumed=True)"


def reset_producer_status(modeladmin, request, queryset):
    """ reset producer status to '-' """
    for qs in queryset:
        if qs.is_active:
            qs.sync_status = '-'
            qs.save()
reset_producer_status.short_description = "Reset producer status to '-'"


def reset_incomingtransaction_error_status(modeladmin, request, queryset):
    """ reset producer status to '-' """
    for qs in queryset:
        qs.is_error = False
        qs.error = None
        qs.save()
reset_incomingtransaction_error_status.short_description = "Reset transaction error status (is_error=False)"

def set_incomingtransaction_as_ignore_status(modeladmin, request, queryset):
    """ set incoming transaction to ignore = true """
    for qs in queryset:
        qs.is_ignored = True
        qs.error = None
        qs.save()
set_incomingtransaction_as_ignore_status.short_description = "Set transaction ignore status (is_ignored=True)"

def reset_incomingtransaction_ignore_status(modeladmin, request, queryset):
    """ set incoming transaction to ignore = false """
    for qs in queryset:
        qs.is_ignored = False
        qs.error = None
        qs.save()
reset_incomingtransaction_ignore_status.short_description = "Reset transaction ignore status (is_ignored=False)"

def decrypt_incomingtransaction(modeladmin, request, queryset):
    """ decrypt the incoming transaction """
    cryptor = FieldCryptor('aes', 'local')
    for qs in queryset:
        tx = cryptor.decrypt(qs.tx)
        qs.tx = tx
        qs.save()
decrypt_incomingtransaction.short_description = "Decrypt the incoming transaction"
