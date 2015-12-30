__author__ = 'Administrator'
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json

class QtsAuthenticationMiddleware(object):
    def process_request(self, request):
        if request.path != '/login/':
            if "username" in request.COOKIES:
                pass
            else:
                if request.method == 'POST':
                    resp_json = {'statusCode': 302}
                    return HttpResponse(json.dumps(resp_json), content_type="application/json")
                else:
                    return HttpResponseRedirect("/login/")
