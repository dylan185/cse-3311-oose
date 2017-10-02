# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View

# Create your views here.

class HomePageView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        # On get guide to home page and load options
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        # On post handle logic
        return render(request, self.template_name, {})