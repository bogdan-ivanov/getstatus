from django.shortcuts import render

from .models import Incident, System


def status(request):
    active = Incident.active.all()
    closed = Incident.closed.all()
    services = System.objects.all()
    return render(request, 'index.html', {
        'active': active,
        'closed': closed,
        'services': services
    })
