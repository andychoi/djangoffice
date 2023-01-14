import string

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import (HttpResponseBadRequest, HttpResponseForbidden,
    HttpResponseRedirect)
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
import json
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from djangoffice.models import Client, Contact, Job
from djangoffice.views import SortHeaders
from djangoffice.views.generic import add_object, edit_object

LIST_HEADERS = (
    (u'Name',         'last_name'),
    (u'Company Name', 'company_name'),
)

# @login_required
# def contact_list(request):
#     """
#     Lists Contacts.
#     """
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     return list_detail.object_list(request,
#         Contact.objects.order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='contact',
#         template_name='contacts/contact_list.html', extra_context={
#             'headers': list(sort_headers.headers()),
#         })

from django.views.generic import list as object_list    #list_detail.object_list
class ContactListView(object_list.ListView):
    template_object_name='contact',
    template_name='contacts/contact_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)

        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        context['headers'] = list(sort_headers.headers())
        return context
    def get_queryset(self):
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        return Client.objects.order_by(sort_headers.get_order_by())


@login_required
def add_contact(request):
    """
    Adds a new Contact.
    """
    return add_object(request, Contact,
        template_name='contacts/add_contact.html')

@login_required
def contact_detail(request, contact_id):
    """
    Displays a Contact's details.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'contacts/contact_detail.html', {
            'contact': contact,
            'activities': contact.activities.select_related(),
        }, )

@login_required
def edit_contact(request, contact_id):
    """
    Edits a Contact.
    """
    return edit_object(request, Contact, contact_id,
        template_object_name='contact',
        template_name='contacts/edit_contact.html')

@login_required
def delete_contact(request, contact_id):
    """
    Deletes a Contact.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    if not contact.is_deleteable:
        return HttpResponseForbidden(u'The selected %s is not deleteable.' \
                                     % Contact._meta.verbose_name)
    return create_update.delete_object(request, Contact,
        post_delete_redirect=reverse('contact_list'), object_id=contact_id,
        template_object_name='contact',
        template_name='contacts/delete_contact.html')

@login_required
def assign_contacts(request, mode):
    """
    Assigns a Contact or Contacts from a pop-up window.
    """
    contacts = Contact.objects.all()

    if mode == 'multiple' and \
       request.GET.get('job_id', None) and \
       Job.objects.filter(pk=request.GET['job_id']).count():
        contacts = contacts.exclude(job_contact_jobs=request.GET['job_id'])
    elif request.GET.get('client_id', None) and \
       Client.objects.filter(pk=request.GET['client_id']).count():
        contacts = contacts.exclude(clients=request.GET['client_id'])

    contact_json = json.dumps([dict(id=c.id, first_name=c.first_name,
        last_name=c.last_name, company_name=c.company_name,
        position=c.position) for c in contacts])
    return render(request, 'contacts/assign_contacts.html', {
            'mode': mode,
            'contact_json': mark_safe(contact_json),
            'letters': string.uppercase,
        }, )
