from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

# Create your views here.
from .forms import EditFlexiTimeForm
from .lib.overtime import get_currrent_weeks_overtime, get_this_weeks_logs
from .models import FlexiTimeLog


# TODO - Implement login / Use the mixin
@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekly_overtime'] = get_currrent_weeks_overtime(self.request.user)

        return context


@method_decorator(login_required, name='dispatch')
class ThisWeek(ListView):
    template_name = 'this_week.html'
    context_object_name = 'flexitime_list'

    def get_queryset(self):
        return get_this_weeks_logs(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_records'] = self.object_list.count()

        return context


class FlexiTimeLogActionMixin:
    form_class = EditFlexiTimeForm
    context_object_name = 'flexitimelog'

    @property
    def success_msg(self):
        return NotImplemented

    def set_form_user(self, form):
        pass

    def form_valid(self, form):
        self.set_form_user(form)
        messages.info(self.request, self.success_msg)

        return super(FlexiTimeLogActionMixin, self).form_valid(form)


class FlexiTimeLogCreateView(FlexiTimeLogActionMixin, CreateView):
    model = FlexiTimeLog
    success_msg = 'FlexiTimeLog created'

    def set_form_user(self, form):
        form.instance.user = self.request.user


class FlexiTimeLogUpdateView(FlexiTimeLogActionMixin, UpdateView):
    model = FlexiTimeLog
    success_msg = 'FlexiTimeLog Updated'


class FlexiTimeLogDetailView(DetailView):
    model = FlexiTimeLog
