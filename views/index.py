from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_section.classes import Section


@login_required
def index(request):
    sections = Section().get_section_list()
    return render_to_response('index.html', {'sections': sections}, context_instance=RequestContext(request))
