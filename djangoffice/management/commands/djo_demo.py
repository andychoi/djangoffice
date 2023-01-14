import logging
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import IntegrityError
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from djangoffice.models import (Client, Contact, ExpenseType, Job, SQLReport,
    Task, TaskType, UserProfile)

class Command(BaseCommand):
    help = 'Prepare demo environment...'

    def handle(self, *args, **options):
        self.create_initial_data()

    # @transaction.commit_on_success
    def create_initial_data(self):
        today = datetime.date.today()

        print('Creating Users')
        admin = self.get_or_create('admin', 'a@a.com', 'demo')
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        UserProfile.objects.filter(user=admin).update(role=UserProfile.ADMINISTRATOR_ROLE)

        testuser = self.get_or_create('testuser', 'tu@tu.com', 'demo')
        testuser.first_name = 'Test'
        testuser.last_name = 'User'
        testuser.save()
        UserProfile.objects.filter(user=testuser).update(role=UserProfile.USER_ROLE)
        testuser.rates.get_or_create(effective_from=today, standard_rate=50.00,
                            overtime_rate=60.00, editable=False)

        testpm = self.get_or_create('testpm', 'tp@tp.com', 'demo')
        testpm.first_name = 'Test'
        testpm.last_name = 'PM'
        testpm.save()
        UserProfile.objects.filter(user=testpm).update(role=UserProfile.PM_ROLE)
        testpm.rates.get_or_create(effective_from=today, standard_rate=60.00,
                            overtime_rate=70.00, editable=False)

        testmanager = self.get_or_create('testmanager', 'tm@tm.com','demo')
        testmanager.first_name = 'Test'
        testmanager.last_name = 'Manager'
        testmanager.save()
        managerprofile = UserProfile.objects.filter(user=testmanager).update(role=UserProfile.MANAGER_ROLE)
        testmanager.userprofile.managed_users.add(testuser)   # manytomany {field}_set
        testmanager.rates.get_or_create(effective_from=today, standard_rate=70.00,
                                overtime_rate=85.00, editable=False)

        print('Creating Admin Client and Contact')
        admin_contact = Contact.objects.create(first_name='Djangoffice',
        last_name='Administrator', company_name=settings.COMPANY_NAME,
        position='Djangoffice Administrator', notes='Required for use by the Admin Job',
        **dict(settings.COMPANY_ADDRESS, **settings.COMPANY_CONTACT))
        company, created = Client.objects.get_or_create(name=settings.COMPANY_NAME,
                                        notes='Required for use by the Admin Job')
        company.contacts.add(admin_contact)

        print('Creating Admin Job')
        admin_job_args = {
            'client': company,
            'name': 'Admin Job',
            'number': 0,
            'status': 'L',
            'director': admin,
            'project_manager': admin,
            'architect': admin,
            'primary_contact': admin_contact,
            'billing_contact': admin_contact,
            'fee_currency': 'GBP',
            # Prevent email notifications on this job
            'missed_end_date': True,
            'over_hours': True,
        }
        admin_job = Job.objects.create(**admin_job_args)

        print('Creating Vacation Task')
        vacation, created = TaskType.objects.get_or_create(name='Vacation')
        vacation_task, created = Task.objects.get_or_create(job=admin_job, task_type=vacation,
                                            estimate_hours=0.0)
        vacation_task.assigned_users.set( [admin, testuser, testpm, testmanager] )
        admin_job.tasks.add(vacation_task)

        print('Creating Task Types')
        task_type_data = (
            ('Programming', 50.00, 50.00),
            ('Requirements', 40.00, 50.00),
            ('Inception', 40.00, 50.00),
            ('Estimation', 40.00, 50.00),
            ('Planning', 40.00, 50.00),
            ('Project Management', 40.00, 50.00),
            ('Change Request', 40.00, 50.00),
            ('Testing', 40.00, 50.00),
            ('Deployment', 40.00, 50.00),
            ('Support', 40.00, 50.00),
            ('Sales Presentations', 60.00, 80.00),
            ('Drawing Plans', 60.00, 80.00),
            ('Lobbying', 75.00, 75.00),
            ('Public Relations', 75.00, 75.00),
        )

        for n, s, o in task_type_data:
            tt = TaskType.objects.create(name=n)
            tt.rates.create(effective_from=today, standard_rate=s, overtime_rate=o,
                            editable=False)

        print('Creating Expense Types')
        expense_type_data = (
            ('Stationary', 'All stationary', 50.00),
            ('Lunches', 'Lunches with customer', 150.00),
            ('Mileage', 'Travel Mileage - 40p per mile', 80.00),
        )
        for n, d, l in expense_type_data:
            ExpenseType.objects.create(name=n, description=d, limit=l)

        print('Creating SQL Reports')
        SQLReport.objects.create(name='Unapproved Time (Up To Date)', access='A',
            query="""SELECT
        t.week_commencing AS 'Week Commencing'
        ,u.username AS 'User'
        ,te.mon + te.tue + te.wed + te.thu + te.fri + te.sat + te.sun AS 'Time Booked'
        ,te.overtime AS 'Overtime Booked'
        FROM
        auth_user u
        INNER JOIN djangoffice_timesheet AS t ON u.id = t.user_id
        INNER JOIN djangoffice_timeentry AS te ON t.id = te.timesheet_id
        WHERE t.week_commencing <= '::UpToDate'
        AND te.approved_by_id IS NULL
        ORDER BY 'Week Commencing' ASC, 'User' ASC""")
        SQLReport.objects.create(name='Unapproved Expenses (Up To Date)',
            access='A',
            query="""SELECT
        e.date AS 'Date'
        ,u.username AS 'User'
        ,j.number AS 'Job Number'
        ,j.name AS 'Job Name'
        ,e.amount AS 'Expense Amount'
        FROM
            auth_user u
            INNER JOIN djangoffice_expensetype AS et ON e.type_id = et.id
            INNER JOIN djangoffice_job AS j ON e.job_id = j.id
            INNER JOIN djangoffice_timesheet AS t ON u.id = t.user_id
            INNER JOIN djangoffice_expense AS e ON t.id = e.timesheet_id
        WHERE e.date <= '::UpToDate'
        AND e.approved_by_id IS NULL
        ORDER BY 'Date' ASC, 'User' ASC""")


    def get_or_create(self, username, email, password, *args, **kwargs):
        try:
            new_user = User.objects.create_user(username, email, password)
        except IntegrityError as e:
            return User.objects.get(username=username, email=email)

        return new_user