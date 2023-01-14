import django.forms.models
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from djangoffice.forms.activities import ActivityFilterForm
from djangoffice.models import Activity, ActivityType, Job
from djangoffice.views import SortHeaders

LIST_HEADERS = (
    (u'Number',      'id'),
    (u'Job',         '%s.number' % Job._meta.db_table),
    (u'Type',        None),
    (u'Created by',  None),
    (u'Created at',  'created_at'),
    (u'Priority',    'priority'),
    (u'Assigned to', None),
    (u'Contact',     None),
    (u'Description', None),
)

from django.views.generic import list

# @login_required
# def activity_list(request):
#     """
#     Lists Activities.

#     A number of filter criteria may be applied to restrict Activities
#     displayed based on a number of factors.
#     """
#     filter_form = ActivityFilterForm(request.GET)
#     filters = filter_form.get_filters()
#     sort_headers = SortHeaders(request, LIST_HEADERS,
#                                additional_params=filter_form.get_params())
#     if filters:
#         queryset = Activity.objects.filter(**filters)
#     else:
#         queryset = Activity.objects.all()
#     # return list_detail.object_list(request, FIXME
#     return list.ListView.as_view(request,
#         queryset.select_related().order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='activity',
#         template_name='activities/activity_list.html', extra_context={
#             'filter_form': filter_form,
#             'headers': list(sort_headers.headers()),
#         })

from django.views.generic import list as object_list    #list_detail.object_list
class ActivityListView(object_list.ListView):
    template_object_name='activity',
    template_name='activities/activity_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)

        filter_form = ActivityFilterForm(self.request.GET)
        sort_headers = SortHeaders(self.request, LIST_HEADERS,
                                additional_params=filter_form.get_params())
        context['filter_form'] = filter_form
        # context['headers'] = list(sort_headers.headers()) #FIXME
        context['headers'] = sort_headers.headers()
        return context

    def get_queryset(self):
        filter_form = ActivityFilterForm(self.request.GET)
        filters = filter_form.get_filters()
        sort_headers = SortHeaders(self.request, LIST_HEADERS,
                                additional_params=filter_form.get_params())
        if filters:
            queryset = Activity.objects.filter(**filters)
        else:
            queryset = Activity.objects.all()        
        return queryset.select_related().order_by(sort_headers.get_order_by())

class AddActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('job', 'type', 'description', 'priority', 'assigned_to',
                  'contact', 'due_date')

@login_required
def add_activity(request):
    """
    Adds an Activity.

    Initial values for any Activity field may be specified as ``GET``
    parameters.
    """

    
    if request.method == 'POST':
        form = AddActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            messages.success(request, 'The %s was created sucessfully.' \
                                      % Activity._meta.verbose_name)
            return HttpResponseRedirect(activity.get_absolute_url())
    else:
        # Fields may be pre-populated with query string parameters
        form = AddActivityForm(initial=dict(request.GET.items()))
    return render(request, 'activities/add_activity.html', {
            'form': form,
        }, )

@login_required
def activity_detail(request, activity_id):
    """
    Displays an Activity's details.
    """
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'activities/activity_detail.html', {
            'activity': activity,
        }, )

class EditActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('job', 'type', 'description', 'priority', 'assigned_to',
                  'contact', 'due_date', 'completed')

@login_required
def edit_activity(request, activity_id):
    """
    Edits an Activity.

    Only Activities which are not marked as completed may be edited.
    """
    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.completed:
        return HttpResponseForbidden(u'Completed %s may not be edited.' \
                                     % Activity._meta.verbose_name_plural)
    if request.method == 'POST':
        form = EditActivityForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save()
            messages.success(request, 'The %s was updated sucessfully.' \
                                      % Activity._meta.verbose_name)
            return HttpResponseRedirect(activity.get_absolute_url())
    else:
        form = EditActivityForm(instance=activity)
    return render(request, 'activities/edit_activity.html', {
            'activity': activity,
            'form': form,
        }, )

@login_required
def delete_activity(request, activity_id):
    """
    Deletes an Activity.
    """
    activity = get_object_or_404(Activity, pk=activity_id)
    return create_update.delete_object(request, Activity,
        post_delete_redirect=reverse('activity_list'), object_id=activity_id,
        template_object_name='activity',
        template_name='activities/delete_activity.html')
