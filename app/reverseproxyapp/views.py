from django.shortcuts import render
from revproxy.views import ProxyView
from .models import AllowedDomain, AttemptedDomainCall
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import Http404

class ReverseProxyView(ProxyView):
    upstream = 'https://orf.at'
    baseUrl = '/proxy/'

    @method_decorator(login_required(login_url='/user/login/'))
    def dispatch(self, request, domain, path):
        print(f'requesting: {domain}/{path}... (request: {request})')
        if AllowedDomain.objects.filter(domain=domain,allow=True).count() < 1:
            print(f'not allowed: {domain}')
            if AttemptedDomainCall.objects.filter(domain=domain).count() < 1:
                AttemptedDomainCall.objects.create(domain=domain,path=path).save()
            raise Http404('Not allowed.')



        self.upstream = f'https://{domain}'
        x = super(ReverseProxyView, self).dispatch(request, path)

        if x.get("Content-Type").split(";")[0] == "text/html":
            if x.__class__.__name__ == "StreamingHttpResponse":
                pass
            else:
                #"(?:(?:https?:\/\/)|(?:\/))([^">]+)"
                import re
                contentData = x.content.decode("utf-8")
                contentData = re.sub(r'"(?:(?:https?:\/\/))([^" >]+)"',self.baseUrl+r'\1',contentData)
                contentData = re.sub(r'"(?:(?:\/))([^">]+)"',self.baseUrl+domain+"/"+r'\1', contentData)
                #x.content = x.content.decode("utf-8").replace("\"/",f"\"{self.baseUrl}{domain}/")
                #x.content = x.content.decode("utf-8").replace("\"http://",f"\"{self.baseUrl}")
                #x.content = x.content.decode("utf-8").replace("\"https://",f"\"{self.baseUrl}")
                x.content = contentData
                contentLen = str(len(contentData))
                print(f'content Length: {contentLen}')
                x._headers['content-length'] = ('Content-Length', contentLen)

        #breakpoint()

        return x