from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

# Create your views here.
from .models import FlexiTimeLog


# TODO - Implement login
@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_records'] = FlexiTimeLog.objects.all().count()

        return context


@method_decorator(login_required, name='dispatch')
class ThisWeek(ListView):
    template_name = 'this_week.html'
    context_object_name = 'flexitime_list'

    def get_queryset(self):
        today = timezone.now().date()
        diff = 0
        # 1 = Monday, 7 = Sunday
        weekday = today.isoweekday()

        if weekday > 1:
            diff = weekday - 1

        monday = today - timedelta(days=diff)

        return FlexiTimeLog.objects.filter(
            user=self.request.user,
            created_at__date__gte=monday,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_records'] = self.object_list.count()

        return context


class FlexiTimeLogCreate(CreateView):
    model = FlexiTimeLog
    fields = ['logged_in', 'break_duration', 'logged_out']

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class FlexiTimeLogUpdate(UpdateView):
    model = FlexiTimeLog
    fields = ['logged_in', 'break_duration', 'logged_out']
