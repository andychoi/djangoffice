from django import forms
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from djangoffice.auth import is_admin_or_manager, user_has_permission
from djangoffice.models import ArtifactType
from djangoffice.views import SortHeaders
from djangoffice.views.generic import add_object, edit_object

LIST_HEADERS = (
    (u'Name',        'name'),
    (u'Description', None),
)

# @user_has_permission(is_admin_or_manager)
# def artifact_type_list(request):
#     """
#     Lists Artifact Types.
#     """
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     return list_detail.object_list(request,
#         ArtifactType.objects.order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='artifact_type',
#         template_name='artifact_types/artifact_type_list.html', extra_context={
#             'headers': list(sort_headers.headers()),
#         })

from django.views.generic import list as object_list    #list_detail.object_list
class ArtifactTypeListView(object_list.ListView):
    template_object_name='artifact_type',
    template_name='artifact_types/artifact_type_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArtifactTypeListView, self).get_context_data(**kwargs)

        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        context['headers'] = list(sort_headers.headers())
        return context
    def get_queryset(self):
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        return ArtifactType.objects.order_by(sort_headers.get_order_by())


@user_has_permission(is_admin_or_manager)
def add_artifact_type(request):
    """
    Adds an Artifact Type.
    """
    return add_object(request, ArtifactType,
        template_name='artifact_types/add_artifact_type.html')

@user_has_permission(is_admin_or_manager)
def artifact_type_detail(request, artifact_type_id):
    """
    Displays an Artifact Type's details.
    """
    artifact_type = get_object_or_404(ArtifactType, pk=artifact_type_id)
    return render(request, 'artifact_types/artifact_type_detail.html', {
            'artifact_type': artifact_type,
        }, )

@user_has_permission(is_admin_or_manager)
def edit_artifact_type(request, artifact_type_id):
    """
    Edits an Artifact Type.
    """
    return edit_object(request, ArtifactType, artifact_type_id,
        template_object_name = 'artifact_type',
        template_name='artifact_types/edit_artifact_type.html')

@user_has_permission(is_admin_or_manager)
def delete_artifact_type(request, artifact_type_id):
    """
    Deletes an Artifact Type.
    """
    artifact_type = get_object_or_404(ArtifactType, pk=artifact_type_id)
    if not artifact_type.is_deleteable:
        return HttpResponseForbidden(u'The selected %s is not deleteable.' \
                                     % ArtifactType._meta.verbose_name)
    return create_update.delete_object(request, ArtifactType,
        post_delete_redirect=reverse('artifact_type_list'),
        object_id=artifact_type_id,
        template_object_name='artifact_type',
        template_name='artifact_types/delete_artifact_type.html')
