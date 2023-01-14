from django import forms
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from djangoffice.auth import is_admin_or_manager, user_has_permission
from djangoffice.models import ActivityType
from djangoffice.views import SortHeaders
from djangoffice.views.generic import add_object, edit_object

LIST_HEADERS = (
    (u'Name',        'name'),
    (u'Access',      'access'),
    (u'Description', None),
)

# @user_has_permission(is_admin_or_manager)
# def activity_type_list(request):
#     """
#     Lists Activity Types.
#     """
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     return list_detail.object_list(request,
#         ActivityType.objects.order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='activity_type',
#         template_name='activity_types/activity_type_list.html', extra_context={
#             'headers': list(sort_headers.headers()),
#         })

from django.views.generic import list as object_list    #list_detail.object_list
class ActivityTypeListView(object_list.ListView):
    template_object_name='activity_type',
    template_name='activity_types/activity_type_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ActivityTypeListView, self).get_context_data(**kwargs)

        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        context['headers'] = list(sort_headers.headers())
        return context
    def get_queryset(self):
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        return ActivityType.objects.order_by(sort_headers.get_order_by())

@user_has_permission(is_admin_or_manager)
def add_activity_type(request):
    """
    Adds an Activity Type.
    """
    return add_object(request, ActivityType,
        template_name='activity_types/add_activity_type.html')

@user_has_permission(is_admin_or_manager)
def activity_type_detail(request, activity_type_id):
    """
    Displays an Activity Type's details.
    """
    activity_type = get_object_or_404(ActivityType, pk=activity_type_id)
    return render(request, 'activity_types/activity_type_detail.html', {
            'activity_type': activity_type,
        }, )

@user_has_permission(is_admin_or_manager)
def edit_activity_type(request, activity_type_id):
    """
    Edits an Activity Type.
    """
    return edit_object(request, ActivityType, activity_type_id,
        template_object_name = 'activity_type',
        template_name='activity_types/edit_activity_type.html')

@user_has_permission(is_admin_or_manager)
def delete_activity_type(request, activity_type_id):
    """
    Deletes an Activity Type.
    """
    activity_type = get_object_or_404(ActivityType, pk=activity_type_id)
    if not activity_type.is_deleteable:
        return HttpResponseForbidden(u'The selected %s is not deleteable.' \
                                     % ActivityType._meta.verbose_name)
    return create_update.delete_object(request, ActivityType,
        post_delete_redirect=reverse('activity_type_list'),
        object_id=activity_type_id,
        template_object_name='activity_type',
        template_name='activity_types/delete_activity_type.html')
