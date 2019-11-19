from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from .models import FlexiTimeLog


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    total_records = FlexiTimeLog.objects.all().count()

    context = {
        'total_records': total_records,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def this_week(request):
    """View function for this weeks rota for the logged in user."""

    # print(request.user.is_authenticated)

    today = timezone.now().date()
    diff = 0
    # 1 = Monday, 7 = Sunday
    weekday = today.isoweekday()

    if weekday > 1:
        diff = weekday - 1

    monday = today - timedelta(days=diff)

    records = FlexiTimeLog.objects.filter(
        user=request.user,
        created_at__date__gte=monday,
    )

    context = {
        'total_records': records.count(),
    }

    return render(request, 'this_week.html', context=context)
