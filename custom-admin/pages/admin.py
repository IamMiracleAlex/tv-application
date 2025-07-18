import threading
import json

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path, reverse
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder

from .mixins import ExportCsvMixin
from .models import MassMail, UserMetric


admin.site.site_header = 'Savests Administration'
User = get_user_model()



@admin.register(UserMetric)
class UserMetricAdmin(admin.ModelAdmin):
    change_list_template = 'admin/usermetric_change_list.html'

    def changelist_view(self, request, extra_context=None):
        # Aggregate new users per day
        chart_data = (
            UserMetric.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        response = super().changelist_view(
            request, extra_context=extra_context,)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Count of all users
        metrics = {
            'total': Count('id'),
        }
    
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response

    def get_urls(self):
        # Url for async data reload
        urls = super().get_urls()
        custom_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return custom_urls + urls


    def chart_data_endpoint(self, request):
        # returns data as json
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        # helper function for aggregating users
        return (
            UserMetric.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )



@admin.register(User)
class MyUserAdmin(UserAdmin, ExportCsvMixin):
    date_hierarchy = 'date_joined'
    
    def full_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).title()

    def update_user(self, obj):
        return format_html('<a class="button" href="/admin/pages/user/{}/change/">Update</a>', obj.id)

    def delete_user(self, obj):
        return format_html('<a class="button" href="/admin/pages/user/{}/delete/">Delete</a>', obj.id)

    def get_urls(self):
        # url for user active status, accepts obj id
        urls = super().get_urls()
        my_urls = [
            path('<int:user_id>/status/', self.admin_site.admin_view(self.status),
                name='status')
        ]
        return my_urls + urls

    def custom_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Change</a>',
            reverse('admin:status', args=[obj.id])
        )
    
    custom_actions.short_description = 'Active Status'

    list_display = ('username','email','full_name','is_active','custom_actions','update_user', 'delete_user')

    actions = ["export_as_csv"]

    ExportCsvMixin.export_as_csv.short_description = 'Export users to csv'
    

    def status(self, request, user_id):
        return self.handle_action(
            request=request,
            user_id=user_id,
        )

    def handle_action(self, request, user_id):
        # change user active status
        user = self.get_object(request, user_id)
        current = user.is_active
        user.is_active = not current
        user.save()
        self.message_user(request, f'Success, "{user.username}" active status has been changed.')
       
        return HttpResponseRedirect(reverse("admin:pages_user_changelist"))
     


class EmailThread(threading.Thread):
    '''Sends users emails by threading. Essential for large user base. This can also be achived using Async, or Task Queue.'''

    def __init__(self, subject, content, recipients):
        self.subject = subject
        self.recipients = recipients
        self.content = content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.content, settings.EMAIL_HOST_USER, self.recipients)
        msg.content_subtype = "html"
        try:
            msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')



class MassMailAdmin(admin.ModelAdmin):
    model = MassMail

    list_display = ('subject','created','author','email_body','updated','custom_actions')
    search_fields = ['subject',]
    list_filter = ['created', 'updated']

    def email_body(self, obj):
        return f'{obj.message}'[:30] + '..'

    def get_urls(self):
        # handles send mail url
        urls = super().get_urls()
        my_urls = [
            path('<int:mail_id>/mail/', self.admin_site.admin_view(self.send_email), name='send_email')
        ]
        return my_urls + urls

    def custom_actions(self, obj):
        # Send mail button
        return format_html(
            '<a class="button" href="{}">Send Mail</a>',
            reverse('admin:send_email', args=[obj.id])
        )
    
    custom_actions.short_description = 'Email all Users'

    def send_email(self, request, mail_id, *args, **kwargs):
        return self.process_mail(
            request=request,
            mail_id=mail_id,
        )

    def process_mail(self, request, mail_id): 
        # get all emails, pass get mail contents and pass them to EmailThread to send email
        
        emails = [ p.email for p in User.objects.all() ] 
        obj = self.get_object(request, mail_id)

        EmailThread(obj.subject, mark_safe(obj.message), emails).start()

        self.message_user(request, f'Success, "{obj.subject}" has been sent to all users.')
       
        return HttpResponseRedirect(reverse("admin:pages_massmail_changelist"))


admin.site.register(MassMail, MassMailAdmin)
