from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import EditFlexiTimeForm
from .models import FlexiTimeLog
from .services.overtime import OvertimeService


class Index(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ot_service = OvertimeService(self.request.user)
        context = super().get_context_data(**kwargs)
        context["weekly_overtime"] = ot_service.get_current_weeks_overtime()

        if ot_service.can_view_all_user_logs():
            context["user_overtime"] = ot_service.get_overtime_for_all_users()

        return context


class ThisWeek(LoginRequiredMixin, ListView):
    template_name = "this_week.html"
    context_object_name = "flexitime_list"

    def get_queryset(self):
        return OvertimeService(self.request.user).get_this_weeks_logs()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_records"] = self.object_list.count()

        return context


@login_required
def edit_today(request: HttpRequest) -> HttpResponse:
    """Either loads the create or update view."""

    try:
        log = _get_todays_log(request)

        # This redirects using FlexiTimeLog.get_absolute_url()
        return redirect(log)
    except FlexiTimeLog.DoesNotExist:
        return redirect("create")


class FlexiTimeLogActionMixin:
    form_class = EditFlexiTimeForm
    context_object_name = "flexitimelog"

    @property
    def success_msg(self):
        return NotImplemented

    def set_form_user(self, form):
        pass

    def form_valid(self, form):
        self.set_form_user(form)
        messages.info(self.request, self.success_msg)

        return super(FlexiTimeLogActionMixin, self).form_valid(form)


class FlexiTimeLogCreateView(LoginRequiredMixin, FlexiTimeLogActionMixin, CreateView):
    model = FlexiTimeLog
    success_msg = "FlexiTimeLog created"

    def set_form_user(self, form):
        form.instance.user = self.request.user


class FlexiTimeLogUpdateView(LoginRequiredMixin, FlexiTimeLogActionMixin, UpdateView):
    model = FlexiTimeLog
    success_msg = "FlexiTimeLog Updated"


class FlexiTimeLogDetailView(LoginRequiredMixin, DetailView):
    model = FlexiTimeLog


@login_required
def edit_week(request: HttpRequest) -> HttpResponse:
    """Edit the weeks rota records... Needs some work."""

    # If we can load today's record do not add a bland row.
    try:
        _get_todays_log(request)
        extra = 0
    except FlexiTimeLog.DoesNotExist:
        extra = 1

    FlextTimeLogFormSet = modelformset_factory(
        FlexiTimeLog, EditFlexiTimeForm, extra=extra
    )

    if request.method == "POST":
        formset = FlextTimeLogFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:
                if form.instance.id is None:
                    form.instance.user = request.user

            formset.save()

        else:
            messages.error(request, "Errors when saving form")
            messages.error(request, formset.errors)

        return redirect("edit_week")

    else:
        queryset = OvertimeService(request.user).get_this_weeks_logs()
        formset = FlextTimeLogFormSet(queryset=queryset)

    return render(
        request, "main/flexitimelog_edit_week.html", context={"formset": formset}
    )


def _get_todays_log(request: HttpRequest) -> FlexiTimeLog:
    """Get today's log record for the logged in user."""

    return FlexiTimeLog.objects.get(user=request.user, log_date=timezone.now().date())
