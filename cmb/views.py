# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.core.urlresolvers import reverse
# from django.views import generic
# from glespy.alm import Alm as galm
# from glespy.tools import convertion as conv


def index(request):
    return render(request, 'cmb/index.html')
