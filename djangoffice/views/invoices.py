from django import forms
from django.conf import settings
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from djangoffice.auth import is_admin_or_manager, user_has_permission
from djangoffice.forms.invoices import (InvoiceFilterForm, InvoiceCriteriaForm,
    SelectJobsForInvoiceForm)
from djangoffice.models import Invoice, Job
from djangoffice.views import send_file, SortHeaders
from djangoffice.views.generic import edit_object
from djangoffice.views.jobs import filter_jobs

LIST_HEADERS = (
    (u'Invoice #',       'number'),
    (u'Invoice Date',    'date'),
    (u'Invoiced From',   'start_period'),
    (u'Invoiced To',     'end_period'),
    (u'Fee Currency',    'job_fee_currency'),
    (u'Amount Invoiced', 'amount_invoiced'),
    (u'Adjustment',      'adjustment'),
    (u'Amount Received', 'amount_received'),
    (u'Job #',           'job_number'),
    (u'Job Name',        'job_name'),
    (u'Client',          'client_name'),
    (u'Primary Contact', None),
    (u'Comment',         None),
)

from django.views.generic import list as object_list

#FIXME
# @user_has_permission(is_admin_or_manager)
# def invoice_list(request):
#     """
#     Lists Invoices.
#     """
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     queryset = Invoice.objects.with_job_details() \
#                                .order_by(sort_headers.get_order_by())
#     return list_detail.object_list(request, queryset,                               
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='invoice',
#         template_name='invoices/invoice_list.html', extra_context={
#             'headers': list(sort_headers.headers()),
#         })
from django.views.generic import list as object_list    #list_detail.object_list
class InvoiceListView(object_list.ListView):
    template_object_name='invoice',
    template_name='invoices/invoice_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)

        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        context['headers'] = list(sort_headers.headers())
        return context

    def get_queryset(self):
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        queryset = Invoice.objects.with_job_details() \
                               .order_by(sort_headers.get_order_by())
        return queryset


@user_has_permission(is_admin_or_manager)
def invoice_wizard(request):
    """
    Manages the two-step process involved in creating invoices:

    1. Display a filterable, orderable list of Jobs which the logged-in
       user has access to, for selection.

    2. Select invoice criteria, using them to previewing an individual
       invoice or create invoices for all selected Jobs.
    """
    if request.method == 'GET':
        step = 1
    else:
        step = int(request.POST.get('step', 1))

    accessible_jobs, filter_form, sort_headers = filter_jobs(request)
    if request.method == 'POST':
        job_form = SelectJobsForInvoiceForm(accessible_jobs, data=request.POST)
        if job_form.is_valid():
            jobs = Job.objects.filter(pk__in=job_form.cleaned_data['jobs'])
            single_job = len(jobs) == 1
            if step == 1: # The select job form has just been submitted
                criteria_form = InvoiceCriteriaForm(jobs)
            else:
                criteria_form = InvoiceCriteriaForm(jobs, data=request.POST)
                if criteria_form.is_valid():
                    if 'create_invoices' in request.POST:
                        return _create_invoices(job_form, criteria_form)
                    else:
                        for job in jobs:
                            if u'draft_invoice%s' % job.id in request.POST:
                                return _create_draft_invoice(job.id,
                                                             criteria_form)
            return render(request, 'invoices/select_invoice_criteria.html', {
                    'form': criteria_form,
                    'job_form': job_form,
                    'jobs': jobs,
                    'single_job': single_job,
                }, )
    else:
        job_form = SelectJobsForInvoiceForm(accessible_jobs)
    return render(request, 'invoices/select_jobs.html', {
            'form': job_form,
            'jobs': accessible_jobs,
            'filter_form': filter_form,
            'headers': list(sort_headers.headers()),
        }, )

# @transaction.commit_on_success
@transaction.atomic
def _create_invoices(job_form, criteria_form):
    """
    Creates invoices for the given Jobs using the given Invoice
    criteria.
    """
    raise NotImplementedError

def _create_draft_invoice(job_id, criteria_form):
    """
    Creates and sends for download a preview of an Invoice PDF for the
    given Job using the given Invoice criteria.
    """
    raise NotImplementedError

@user_has_permission(is_admin_or_manager)
def invoice_detail(request, invoice_number):
    """
    Displays an Invoice's details.
    """
    invoice = get_object_or_404(Invoice.objects.with_job_details(),
                                number=invoice_number)
    return render(request, 'invoices/invoice_detail.html', {
            'invoice': invoice,
        }, )

@user_has_permission(is_admin_or_manager)
def edit_invoice(request, invoice_number):
    """
    Edits an Invoice.
    """
    invoice = get_object_or_404(Invoice.objects.with_job_details(),
                                number=invoice_number)
    return edit_object(request, Invoice, invoice.id,
        fields=('adjustment', 'amount_received', 'comment'),
        template_object_name='invoice',
        template_name='invoices/edit_invoice.html', extra_context={
            'invoice': invoice,
        })

@user_has_permission(is_admin_or_manager)
def download_invoice(request, invoice_number):
    """
    Sends the PDF associated with the given Invoice for download.
    """
    invoice = get_object_or_404(Invoice, number=invoice_number)
    return send_file(invoice.get_pdf_filename())

@user_has_permission(is_admin_or_manager)
def delete_invoice(request, invoice_number):
    """
    Deletes the given Invoice.
    """
    invoice = get_object_or_404(Invoice, number=invoice_number)
    return create_update.delete_object(request, Invoice,
        post_delete_redirect=reverse('invoice_list'),
        object_id=invoice.pk, template_object_name='invoice',
        template_name='invoices/delete_invoice.html')
