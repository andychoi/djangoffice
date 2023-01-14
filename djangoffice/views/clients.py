from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from djangoffice.auth import is_admin_or_manager, user_has_permission
from djangoffice.models import Client, Job
from djangoffice.views import SortHeaders
from djangoffice.views.generic import add_object, edit_object

LIST_HEADERS = (
    (u'Client', 'name'),
)

# @login_required
# def client_list(request):
#     """
#     Lists Clients.
#     """
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     return list_detail.object_list(request,
#         Client.objects.order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='client',
#         template_name='clients/client_list.html', extra_context={
#             'headers': list(sort_headers.headers()),
#         })

from django.views.generic import list as object_list    #list_detail.object_list
class ClientListView(object_list.ListView):
    template_object_name='client',
    template_name='clients/client_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)

        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        context['headers'] = list(sort_headers.headers())
        return context
    def get_queryset(self):
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        return Client.objects.order_by(sort_headers.get_order_by())



@login_required
def add_client(request):
    """
    Adds a Client.
    """
    return add_object(request, Client, fields=('name', 'notes'),
        template_name='clients/add_client.html')


@login_required
def client_detail(request, client_id):
    """
    Displays a Client's details.
    """
    client = get_object_or_404(Client, pk=client_id)
    jobs = Job.objects.accessible_to_user(request.user) \
                       .filter(client=client).order_by('number')
    return render(request, 'clients/client_detail.html', {
            'client': client,
            'jobs': jobs,
            'contacts': client.contacts.all(),
        }, )

@login_required
def edit_client(request, client_id):
    """
    Edit a Client.
    """
    return edit_object(request, Client, client_id,
        fields=('name', 'notes', 'disabled'),
        template_name='clients/edit_client.html',
        template_object_name='client')

@user_has_permission(is_admin_or_manager)
def delete_client(request, client_id):
    """
    Deletes a Client.
    """
    client = get_object_or_404(Client, pk=client_id)
    if not client.is_deleteable:
        return HttpResponseForbidden(u'The selected %s is not deleteable.' \
                                     % Client._meta.verbose_name)
    return create_update.delete_object(request, Client,
        post_delete_redirect=reverse('client_list'), object_id=client_id,
        template_object_name='client',
        template_name='clients/delete_client.html')
