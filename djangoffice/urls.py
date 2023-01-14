from django.urls import path, re_path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
from .views import users, clients, contacts, task_types, jobs, artifact_types, artifacts, activities, expense_types, activity_types, timesheets, invoices, reports, sql_reports
from .views.users import UserListView
from .views.clients import ClientListView
from .views.contacts import ContactListView
from .views.task_types import TaskTypeListView
from .views.jobs import JobListView
from .views.artifact_types import ArtifactTypeListView
from .views.artifacts import ArtifactListView
from .views.activities import ActivityListView
from .views.expense_types import ExpenseTypeListView
from .views.activity_types import ActivityTypeListView
# from .views.timesheets import TimesheetListView
from .views.invoices import InvoiceListView
# from .views.reports import ReportListView
from .views.sql_reports import SQLReportListView
admin.site.enable_nav_sidebar = True

TIMESHEET_BASE = r'timesheets/(?P<username>[-\w]+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'

urlpatterns = [ #patterns(
    # path('', djangoffice.views, ),# 'djangoffice.views',
    # re_path(r'^$', users.login),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logged_out.html'), name = 'logout'),    

    # Users
    # re_path(r'^login/$',                                users.login,           name='login'),
    # re_path(r'^logout/$',                               users.logout,          name='logout'),
    re_path(r'^users/$',                                UserListView.as_view(),       name='user_list'),
    re_path(r'^users/editadmin/$',                      users.edit_admin_user, name='edit_admin_user'),
    re_path(r'^users/add/$',                            users.add_user,        name='add_user'),
    re_path(r'^users/(?P<username>[-\w]+)/$',           users.user_detail,     name='user_detail'),
    re_path(r'^users/(?P<username>[-\w]+)/edit/$',      users.edit_user,       name='edit_user'),
    re_path(r'^users/(?P<username>[-\w]+)/rates/$',     users.edit_user_rates, name='edit_user_rates'),
    re_path(r'^users/(?P<username>[-\w]+)/rates/add/$', users.add_user_rate,   name='add_user_rate'),
    re_path(r'^users/(?P<username>[-\w]+)/delete/$',    users.delete_user,     name='delete_user'),

    # Clients
    re_path(r'^clients/$',                             ClientListView.as_view(),   name='client_list'),
    re_path(r'^clients/add/$',                         clients.add_client,    name='add_client'),
    re_path(r'^clients/(?P<client_id>\d+)/$',          clients.client_detail, name='client_detail'),
    re_path(r'^clients/(?P<client_id>\d+)/edit/$',     clients.edit_client,   name='edit_client'),
    re_path(r'^clients/(?P<client_id>\d+)/delete/$',   clients.delete_client, name='delete_client'),

    # Contacts
    re_path(r'^contacts/$',                                  ContactListView.as_view(),    name='contact_list'),
    re_path(r'^contacts/add/$',                              contacts.add_contact,     name='add_contact'),
    re_path(r'^contacts/(?P<contact_id>\d+)/$',              contacts.contact_detail,  name='contact_detail'),
    re_path(r'^contacts/(?P<contact_id>\d+)/edit/$',         contacts.edit_contact,    name='edit_contact'),
    re_path(r'^contacts/(?P<contact_id>\d+)/delete/$',       contacts.delete_contact,  name='delete_contact'),
    re_path(r'^contacts/assign/(?P<mode>single|multiple)/$', contacts.assign_contacts, name='assign_contacts'),

    # Task Types
    re_path(r'^task_types/$',                                 TaskTypeListView.as_view(),       name='task_type_list'),
    re_path(r'^task_types/add/$',                             task_types.add_task_type,        name='add_task_type'),
    re_path(r'^task_types/(?P<task_type_id>\d+)/$',           task_types.task_type_detail,     name='task_type_detail'),
    re_path(r'^task_types/(?P<task_type_id>\d+)/edit/$',      task_types.edit_task_type,       name='edit_task_type'),
    re_path(r'^task_types/(?P<task_type_id>\d+)/rates/$',     task_types.edit_task_type_rates, name='edit_task_type_rates'),
    re_path(r'^task_types/(?P<task_type_id>\d+)/rates/add/$', task_types.add_task_type_rate,   name='add_task_type_rate'),
    re_path(r'^task_types/(?P<task_type_id>\d+)/delete/$',    task_types.delete_task_type,     name='delete_task_type'),

    # Jobs
    re_path(r'^jobs/$',                                    JobListView.as_view(),           name='job_list'),
    re_path(r'^jobs/add/$',                                jobs.add_job,            name='add_job'),
    re_path(r'^jobs/(?P<job_number>\d+)/$',                jobs.job_detail,         name='job_detail'),
    re_path(r'^jobs/(?P<job_number>\d+)/edit/$',           jobs.edit_job,           name='edit_job'),
    re_path(r'^jobs/(?P<job_number>\d+)/delete/$',         jobs.delete_job,         name='delete_job'),
    re_path(r'^jobs/(?P<job_number>\d+)/previewquote/$',   jobs.preview_job_quote,  name='preview_job_quote'),
    re_path(r'^jobs/(?P<job_number>\d+)/generatewquote/$', jobs.generate_job_quote, name='generate_job_quote'),

    # Artifacts
    re_path(r'^jobs/(?P<job_number>\d+)/artifacts/$',                               ArtifactListView.as_view(),     name='artifact_list'),
    re_path(r'^jobs/(?P<job_number>\d+)/artifacts/add/$',                           artifacts.add_artifact,      name='add_artifact'),
    re_path(r'^jobs/(?P<job_number>\d+)/artifacts/(?P<artifact_id>\d+)/$',          artifacts.artifact_detail,   name='artifact_detail'),
    re_path(r'^jobs/(?P<job_number>\d+)/artifacts/(?P<artifact_id>\d+)/download/$', artifacts.download_artifact, name='download_artifact'),
    re_path(r'^jobs/(?P<job_number>\d+)/artifacts/(?P<artifact_id>\d+)/edit/$',     artifacts.edit_artifact,     name='edit_artifact'),
    re_path(r'^jobs/(?P<job_number>\d+)/artifacts/(?P<artifact_id>\d+)/delete/$',   artifacts.delete_artifact,   name='delete_artifact'),

    # Activities
    re_path(r'^activities/$',                               ActivityListView.as_view(),   name='activity_list'),
    re_path(r'^activities/add/$',                           activities.add_activity,    name='add_activity'),
    re_path(r'^activities/(?P<activity_id>\d+)/$',          activities.activity_detail, name='activity_detail'),
    re_path(r'^activities/(?P<activity_id>\d+)/edit/$',     activities.edit_activity,   name='edit_activity'),
    re_path(r'^activities/(?P<activity_id>\d+)/delete/$',   activities.delete_activity, name='delete_activity'),

    # Expense Types
    re_path(r'^expense_types/$',                                 ExpenseTypeListView.as_view(),   name='expense_type_list'),
    re_path(r'^expense_types/add/$',                             expense_types.add_expense_type,    name='add_expense_type'),
    re_path(r'^expense_types/(?P<expense_type_id>\d+)/$',        expense_types.expense_type_detail, name='expense_type_detail'),
    re_path(r'^expense_types/(?P<expense_type_id>\d+)/edit/$',   expense_types.edit_expense_type,   name='edit_expense_type'),
    re_path(r'^expense_types/(?P<expense_type_id>\d+)/delete/$', expense_types.delete_expense_type, name='delete_expense_type'),

    # Activity Types
    re_path(r'^activity_types/$',                                  ActivityTypeListView.as_view(),   name='activity_type_list'),
    re_path(r'^activity_types/add/$',                              activity_types.add_activity_type,    name='add_activity_type'),
    re_path(r'^activity_types/(?P<activity_type_id>\d+)/$',        activity_types.activity_type_detail, name='activity_type_detail'),
    re_path(r'^activity_types/(?P<activity_type_id>\d+)/edit/$',   activity_types.edit_activity_type,   name='edit_activity_type'),
    re_path(r'^activity_types/(?P<activity_type_id>\d+)/delete/$', activity_types.delete_activity_type, name='delete_activity_type'),

    # Artifact Types
    re_path(r'^artifact_types/$',                                  ArtifactTypeListView.as_view(),   name='artifact_type_list'),
    re_path(r'^artifact_types/add/$',                              artifact_types.add_artifact_type,    name='add_artifact_type'),
    re_path(r'^artifact_types/(?P<artifact_type_id>\d+)/$',        artifact_types.artifact_type_detail, name='artifact_type_detail'),
    re_path(r'^artifact_types/(?P<artifact_type_id>\d+)/edit/$',   artifact_types.edit_artifact_type,   name='edit_artifact_type'),
    re_path(r'^artifact_types/(?P<artifact_type_id>\d+)/delete/$', artifact_types.delete_artifact_type, name='delete_artifact_type'),

    # Timesheets
    re_path(r'^timesheets/$',                                                     timesheets.timesheet_index,       name='timesheet_index'),
    re_path(r'^timesheets/bulk_approval/$',                                       timesheets.bulk_approval,         name='bulk_approval'),
    re_path(r'^%s/$' % TIMESHEET_BASE,                                            timesheets.edit_timesheet,        name='edit_timesheet'),
    re_path(r'^%s/approve/' % TIMESHEET_BASE,                                     timesheets.approve_timesheet,     name='approve_timesheet'),
    re_path(r'^%s/prepopulate/$' % TIMESHEET_BASE,                                timesheets.prepopulate_timesheet, name='prepopulate_timesheet'),
    re_path(r'^%s/time_entries/add/$' % TIMESHEET_BASE,                           timesheets.add_time_entry,        name='add_time_entry'),
    re_path(r'^%s/time_entries/(?P<time_entry_id>\d+)/delete/$' % TIMESHEET_BASE, timesheets.delete_time_entry,     name='delete_time_entry'),
    re_path(r'^%s/expenses/add/$' % TIMESHEET_BASE,                               timesheets.add_expense,           name='add_expense'),
    re_path(r'^%s/expenses/(?P<expense_id>\d+)/delete/$' % TIMESHEET_BASE,        timesheets.delete_expense,        name='delete_expense'),

    # Invoices
    re_path(r'^invoices/$',                                  InvoiceListView.as_view(),     name='invoice_list'),
    re_path(r'^invoices/create/$',                           invoices.invoice_wizard,   name='create_invoices'),
    re_path(r'^invoices/(?P<invoice_number>\d+)/$',          invoices.invoice_detail,   name='invoice_detail'),
    re_path(r'^invoices/(?P<invoice_number>\d+)/edit/$',     invoices.edit_invoice,     name='edit_invoice'),
    re_path(r'^invoices/(?P<invoice_number>\d+)/download/$', invoices.download_invoice, name='download_invoice'),
    re_path(r'^invoices/(?P<invoice_number>\d+)/delete/$',   invoices.delete_invoice,   name='delete_invoice'),

    # Reports
    re_path(r'^reports/$',                    reports.report_list,               name='report_list'),
    re_path(r'^reports/annual_leave/$',       reports.annual_leave_report,       name='annual_leave_report'),
    re_path(r'^reports/client/$',             reports.client_report,             name='client_report'),
    re_path(r'^reports/developer_progress/$', reports.developer_progress_report, name='developer_progress_report'),
    re_path(r'^reports/invoiced_work/$',      reports.invoiced_work_report,      name='invoiced_work_report'),
    re_path(r'^reports/job_expenses/$',       reports.job_expenses_report,       name='job_expenses_report'),
    re_path(r'^reports/job_full/$',           reports.job_full_report,           name='job_full_report'),
    re_path(r'^reports/job_list/$',           reports.job_list_report,           name='job_list_report'),
    re_path(r'^reports/job_list_summary/$',   reports.job_list_summary_report,   name='job_list_summary_report'),
    re_path(r'^reports/job_reports/$',        reports.job_report_list,           name='job_report_list'),
    re_path(r'^reports/job_status/$',         reports.job_status_report,         name='job_status_report'),
    re_path(r'^reports/jobs_missingdata/$',   reports.jobs_missing_data_report,  name='jobs_missing_data_report'),
    re_path(r'^reports/jobs_worked_on/$',     reports.jobs_worked_on_report,     name='jobs_worked_on_report'),
    re_path(r'^reports/timesheet/$',          reports.timesheet_report,          name='timesheet_report'),
    re_path(r'^reports/timesheet_reports/$',  reports.report_list,               name='timesheet_report_list'),
    re_path(r'^reports/timesheet_status/$',   reports.timesheet_status_report,   name='timesheet_status_report'),
    re_path(r'^reports/uninvoiced_work/$',    reports.uninvoiced_work_report,    name='uninvoiced_work_report'),
    re_path(r'^reports/user/$',               reports.user_report,               name='user_report'),

    # SQL Reports
    re_path(r'^sql_reports/$',                                SQLReportListView.as_view(),    name='sql_report_list'),
    re_path(r'^sql_reports/add/$',                            sql_reports.add_sql_report,     name='add_sql_report'),
    re_path(r'^sql_reports/(?P<sql_report_id>\d+)/$',         sql_reports.sql_report_detail,  name='sql_report_detail'),
    re_path(r'^sql_reports/(?P<sql_report_id>\d+)/edit/$',    sql_reports.edit_sql_report,    name='edit_sql_report'),
    re_path(r'^sql_reports/(?P<sql_report_id>\d+)/delete/$',  sql_reports.delete_sql_report,  name='delete_sql_report'),
    re_path(r'^sql_reports/(?P<sql_report_id>\d+)/execute/$', sql_reports.execute_sql_report, name='execute_sql_report'),
]

# Admin and settings applications
urlpatterns += [
    # '',
    #(r'^admin/', include('django.contrib.admin.urls')),
    re_path(r'^settings/', include('dbsettings.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^admin/', admin.site.urls, name="admin")
] 