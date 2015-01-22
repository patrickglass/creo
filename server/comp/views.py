from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Comp


def index(request, active_only=False, chip_only=True):
    comps = Comp.objects.order_by('name')

    return render_to_response('index.html',
                              {'list': comps},
                              context_instance=RequestContext(request))
