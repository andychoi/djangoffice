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
from djangoffice.models import ExpenseType
from djangoffice.views import SortHeaders
from djangoffice.views.generic import add_object, edit_object

LIST_HEADERS = (
    (u'Name',        'name'),
    (u'Description', None),
    (u'Limit',       'limit'),
)

# @user_has_permission(is_admin_or_manager)
# def expense_type_list(request):
#     """
#     Lists Expense Types.
#     """
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     return list_detail.object_list(request,
#         ExpenseType.objects.order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='expense_type',
#         template_name='expense_types/expense_type_list.html', extra_context={
#             'headers': list(sort_headers.headers()),
#         })
from django.views.generic import list as object_list    #list_detail.object_list
class ExpenseTypeListView(object_list.ListView):
    template_object_name='expense_type',
    template_name='expense_types/expense_type_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ExpenseTypeListView, self).get_context_data(**kwargs)

        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        context['headers'] = list(sort_headers.headers())
        return context
    def get_queryset(self):
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        return ExpenseType.objects.order_by(sort_headers.get_order_by())


@user_has_permission(is_admin_or_manager)
def add_expense_type(request):
    """
    Adds an Expense Type.
    """
    return add_object(request, ExpenseType,
        template_name='expense_types/add_expense_type.html')

@user_has_permission(is_admin_or_manager)
def expense_type_detail(request, expense_type_id):
    """
    Displays an Expense Type's details.
    """
    expense_type = get_object_or_404(ExpenseType, pk=expense_type_id)
    return render(request, 'expense_types/expense_type_detail.html', {
            'expense_type': expense_type,
        }, )

@user_has_permission(is_admin_or_manager)
def edit_expense_type(request, expense_type_id):
    """
    Edits an Expense Type.
    """
    return edit_object(request, ExpenseType, expense_type_id,
        template_object_name = 'expense_type',
        template_name='expense_types/edit_expense_type.html')

@user_has_permission(is_admin_or_manager)
def delete_expense_type(request, expense_type_id):
    """
    Deletes an Expense Type.
    """
    expense_type = get_object_or_404(ExpenseType, pk=expense_type_id)
    if not expense_type.is_deleteable:
        return HttpResponseForbidden(u'The selected %s is not deleteable.' \
                                     % ExpenseType._meta.verbose_name)
    return create_update.delete_object(request, ExpenseType,
        post_delete_redirect=reverse('expense_type_list'),
        object_id=expense_type_id,
        template_object_name='expense_type',
        template_name='expense_types/delete_expense_type.html')
