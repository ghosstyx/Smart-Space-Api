from django.shortcuts import render
from .models import *
def adm():
    # workhours = WorkHours.objects.all()
    # marktrack = MarkTrack.objects.all()
    # context = {"workhours": workhours, "marktrack": marktrack}
    # if workhours.arrive < marktrack.arrival:
    #     marktrack.is_late = True
    # else:
    #     marktrack.is_late = False
    return render(request, '', context=context)
