# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render

from external_api import external_api_manager
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def receiver_view(request, manufacture, name):
    # import ipdb; ipdb.set_trace()
    if manufacture not in external_api_manager.receiver_functions:
        raise Http404("Manufacture {} does not exist".format(manufacture))

    if name not in external_api_manager.receiver_functions[manufacture]['names']:
        raise Http404("Name {} from manufacture {} does not exist".format(name, manufacture))

    receiver_name = "receiver_{}".format(name)
    api = external_api_manager.receiver_functions[manufacture]["__api_class__"]()
    func = getattr(api, receiver_name)

    try:
        func(request)
        return HttpResponse()
    except Exception:
        return HttpResponseServerError()
