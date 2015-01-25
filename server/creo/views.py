from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Field, Config, Entry


def config_index(request, active_only=False, chip_only=True):
    comps = Config.objects.order_by('name')

    return render_to_response('index.html',
                              {'list': comps},
                              context_instance=RequestContext(request))


def config_display(request, id):
    obj = Config.objects.get(id=id)

    return render_to_response('index.html',
                              {'item': obj},
                              context_instance=RequestContext(request))


def field_index(request, active_only=False, chip_only=True):
    comps = Comp.objects.order_by('name')

    return render_to_response('index.html',
                              {'list': comps},
                              context_instance=RequestContext(request))


def field_display(request, id):
    obj = Field.objects.get(id=id)

    return render_to_response('index.html',
                              {'item': obj},
                              context_instance=RequestContext(request))
