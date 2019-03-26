from django.shortcuts import render
from django.views.generic import TemplateView
from .models import menuItem


class PraaSPortalView(TemplateView):
    template_name = 'praas/template_base.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qryObj = menuItem.objects.all()
        if self.request.user.get_username():
            qryObj = qryObj.filter(onlyDisplayIfLoggedOut=False)
        else:
            qryObj = qryObj.filter(requiresLogin=False)

        context["menuitems"] = []
        for obj in qryObj:
            context["menuitems"].append({"href": obj.href, "description": obj.description})


        return context
        