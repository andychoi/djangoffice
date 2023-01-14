import datetime

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
# from django.views.generic import list_detail
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from djangoffice.models import Artifact, Job
from djangoffice.views import permission_denied, send_file, SortHeaders
from djangoffice.views.generic import add_object, edit_object

LIST_HEADERS = (
    (u'Description', None),
    (u'Type',        None),
    (u'File',        'file'),
    (u'Size',        None),
    (u'Created At',  'created_at'),
    (u'Updated At',  'updated_at'),
    (u'Access',      'access'),
)

# @login_required
# def artifact_list(request, job_number):
#     """
#     Lists Artifacts for the Job with the given number.

#     Only list Atrifacts which the logged-in user has access to, based on
#     their role and the access type set on each Artifact.
#     """
#     job = get_object_or_404(Job, number=int(job_number))
#     if not job.is_accessible_to_user(request.user):
#         return permission_denied(request)
#     user_profile = request.user.userprofile
#     queryset = Artifact.objects.accessible_to_user(request.user).filter(job=job)
#     sort_headers = SortHeaders(request, LIST_HEADERS)
#     return list_detail.object_list(request,
#         queryset.order_by(sort_headers.get_order_by()),
#         paginate_by=settings.ITEMS_PER_PAGE, allow_empty=True,
#         template_object_name='artifact',
#         template_name='artifacts/artifact_list.html', extra_context={
#             'job': job,
#             'headers': list(sort_headers.headers()),
#         })


from django.views.generic import list as object_list    #list_detail.object_list
class ArtifactListView(object_list.ListView):
    template_object_name='artifact',
    template_name='artifacts/artifact_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArtifactListView, self).get_context_data(**kwargs)
        job_number = kwargs.get('job_number', None)
        
        if job_number:
            job = get_object_or_404(Job, number=int(job_number))
            sort_headers = SortHeaders(self.request, LIST_HEADERS)
            context['job'] = job
            context['headers'] = list(sort_headers.headers())
        return context

    def get_queryset(self):
        job_number = self.kwargs['job_number']
        
        job = get_object_or_404(Job, number=int(job_number))
        sort_headers = SortHeaders(self.request, LIST_HEADERS)
        if not job.is_accessible_to_user(self.request.user):
            return permission_denied(self.request)
        user_profile = self.request.user.userprofile
        queryset = Artifact.objects.accessible_to_user(self.request.user).filter(job=job)
        return queryset.order_by(sort_headers.get_order_by()),

class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        fields= ('file', 'type', 'description', 'access')

@login_required
def add_artifact(request, job_number):
    """
    Adds an Artifact.
    """
    job = get_object_or_404(Job, number=int(job_number))
    if not job.is_accessible_to_user(request.user):
        return permission_denied(request)
    if request.method == 'POST':
        form = ArtifactForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            artifact = form.save(commit=False)
            artifact.job = job
            artifact.created_at = datetime.datetime.now()
            artifact.updated_at = artifact.created_at
            artifact.save()
            messages.success(request, 'The %s was added successfully.' \
                                      % Artifact._meta.verbose_name)
            return HttpResponseRedirect(reverse('artifact_list',
                                                args=(job_number,)))
    else:
        form = ArtifactForm()
    return render(request, 'artifacts/add_artifact.html', {
            'form': form,
            'job': job,
        }, )

@login_required
def artifact_detail(request, job_number, artifact_id):
    """
    Displays an Artifact's details.
    """
    job = get_object_or_404(Job, number=int(job_number))
    artifact = get_object_or_404(Artifact, job=job, pk=artifact_id)
    if not job.is_accessible_to_user(request.user) or \
       not artifact.is_accessible_to_user(request.user):
        return permission_denied(request)
    return render(request, 'artifacts/artifact_detail.html', {
        'artifact': artifact,
        'job': job,
    }, )

@login_required
def download_artifact(request, job_number, artifact_id):
    """
    Sends an Artifact for download.
    """
    artifact = get_object_or_404(Artifact.objects.accessible_to_user(request.user),
                                 pk=artifact_id)
    return send_file(artifact.get_file_filename())

@login_required
def edit_artifact(request, job_number, artifact_id):
    """
    Edits an Artifact.
    """
    job = get_object_or_404(Job, number=int(job_number))
    artifact = get_object_or_404(Artifact, job=job, pk=artifact_id)
    if not job.is_accessible_to_user(request.user) or \
       not artifact.is_accessible_to_user(request.user):
        return permission_denied(request)
    if request.method == 'POST':
        form = ArtifactForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            artifact = form.save(commit=False)
            artifact.updated_at = datetime.datetime.now()
            artifact.save()
            messages.success(request, 'The %s was edited successfully.' \
                                      % Artifact._meta.verbose_name)
            return HttpResponseRedirect(reverse('artifact_list',
                                        args=(job_number,)))
    else:
        form = ArtifactForm()
    return render(request, 'artifacts/edit_artifact.html', {
            'form': form,
            'artifact': artifact,
            'job': job,
        }, )

@login_required
def delete_artifact(request, job_number, artifact_id):
    """
    Deletes an Artifact.
    """
    raise NotImplementedError
