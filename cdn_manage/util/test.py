__author__ = 'liujiahua'
import httplib
import logging
LOG = logging.getLogger(__name__)
console = logging.StreamHandler()
LOG.addHandler(console)

def req(rq_body=''):
    rq_headers = {"Content-type": 'application/json',
                  'X-Auth-Token': '60feb5797e974a89af19e9a40f04ac07'}
    try:
        httpClient = httplib.HTTPConnection('127.0.0.9:5000',timeout=3)
        httpClient.request('GET', '/cdn_api/req_status/e2ee9800-9032-11e5-a35f-e03f4978b2ff', rq_body, rq_headers)
        response = httpClient.getresponse()
        httpClient.close()
        return response
    except Exception, e:
        LOG.error('Could not connect to api_server %s' % e)

res = req()

