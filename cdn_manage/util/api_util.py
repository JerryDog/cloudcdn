# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
import json
import logging
LOG = logging.getLogger(__name__)
import httplib
import traceback, sys
from django.conf import settings
from collections import OrderedDict

def getTokenFromKS(username, password):
    headers = {"Content-type": "application/json"}
    KEYSTONE = settings.KEYSTONE
    try:
        conn = httplib.HTTPConnection(KEYSTONE)
    except:
        return 'ConnError'
    params = '{"auth": {"passwordCredentials": {"username": "%s", "password": "%s"}}}' % (username, password)
    try:
        conn.request("POST", "/v2.0/tokens", params, headers)
    except:
        return 'ConnError'
    response = conn.getresponse()
    data = response.read()
    dd = json.loads(data)
    try:
        apitoken = dd['access']['token']['id']
    except:
        return None, None
    user_id = dd['access']['user']['id']
    rq_headers = {"X-Auth-Token": "%s" % apitoken}
    conn.request('GET', '/v3/users/%s/projects' % user_id, '', rq_headers)
    resp = conn.getresponse().read()
    result = json.loads(resp)
    project_list = []
    for p in result["projects"]:
        l = [p["name"], p["id"]]
        project_list.append(l)
    conn.close()
    return project_list, apitoken


def domain_to_json(domain, project_id=None, username=None):
    domain_dict = {"domain": {
        "domainName": domain.domain_name,
        "testUrl": domain.test_url,
        "originIps": domain.origin_ips,
    }, "projectId": project_id, "username": username}

    # 建站必须的3个属性
    if domain.service_type:
        domain_dict["domain"]["serviceType"] = domain.service_type
    if domain.comment:
        domain_dict["domain"]["comment"] = domain.comment
    if domain.enabled:
        domain_dict["domain"]["enabled"] = domain.enabled

    # 编辑站必须的 domain_id
    if domain.domain_id:
        domain_dict["domain"]["domainId"] = domain.domain_id

    if domain.cache_behaviors:
        items = domain.cache_behaviors.split(';')
        cache_rules = []
        for item in items:
            cache = item.split(',')
            cache_rule = {}
            cache_rule["pathPattern"] = cache[0]
            cache_rule["ignoreCacheControl"] = cache[1]
            cache_rule["cacheTtl"] = cache[2]
            cache_rules.append(cache_rule)
        domain_dict["domain"]["cacheBehaviors"] = cache_rules

    return json.JSONEncoder().encode(domain_dict)


class DomainApi(object):
    def __init__(self, token):
        self.token = token

    def add(self, domain, project_id=None, username=None):
        rq_url = '/cdn_api/add'
        method = 'POST'
        rq_body = domain_to_json(domain, project_id, username)
        res = self.req(method, rq_url, rq_body)
        LOG.info("AddDomain Request Url: %s" % rq_url)
        LOG.info("AddDomain status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("AddDomain Body: %s" % rq_body)
        return res

    def modify(self, domain):
        rq_url = '/cdn_api/modify'
        method = 'PUT'
        rq_body = domain_to_json(domain)
        res = self.req(method, rq_url, rq_body)
        LOG.info("ModifyDomain Request Url: %s" % rq_url)
        LOG.info("ModifyDomain status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("ModifyDomain Body: %s" % rq_body)
        return res

    def delete(self, domain_id):
        rq_url = '/cdn_api/delete/%s' % domain_id
        method = 'DELETE'
        rq_body = ''
        res = self.req(method, rq_url, rq_body)
        LOG.info("DeleteDomain Request Url: %s" % rq_url)
        LOG.info("DeleteDomain status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("DeleteDomain Body: %s" % rq_body)
        return res

    def find(self, domain_id):
        rq_url = '/cdn_api/find/%s' % domain_id
        method = 'GET'
        rq_body = ''
        res = self.req(method, rq_url, rq_body)
        LOG.info("FindDomain Request Url: %s" % rq_url)
        LOG.info("FindDomain status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("FindDomain Body: %s" % rq_body)
        return res

    def purge(self, json_str):
        rq_url = '/cdn_api/purge'
        method = 'POST'
        rq_body = json.JSONEncoder().encode(json_str)
        res = self.req(method, rq_url, rq_body)
        LOG.info("Purge Request Url: %s" % rq_url)
        LOG.info("Purge status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("Purge Body: %s" % rq_body)
        return res

    def prefetch(self, json_str):
        rq_url = '/cdn_api/prefetch'
        method = 'POST'
        rq_body = json.JSONEncoder().encode(json_str)
        res = self.req(method, rq_url, rq_body)
        LOG.info("Prefetch Request Url: %s" % rq_url)
        LOG.info("Prefetch status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("Prefetch Body: %s" % rq_body)
        return res

    def req_status(self, task_id):
        rq_url = '/cdn_api/req_status/%s' % task_id
        method = 'GET'
        rq_body = ''
        res = self.req(method, rq_url, rq_body)
        LOG.info("ReqStatus Request Url: %s" % rq_url)
        LOG.info("ReqStatus status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("ReqStatus Body: %s" % rq_body)
        return res

    def flow(self, json_str):
        rq_url = '/cdn_api/flow'
        method = 'GET'
        rq_body = json.JSONEncoder().encode(json_str)
        res = self.req(method, rq_url, rq_body)
        LOG.info("Flow Request Url: %s" % rq_url)
        LOG.info("Flow status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("Flow Body: %s" % rq_body)
        return res

    def bandwidth(self, json_str):
        rq_url = '/cdn_api/bandwidth'
        method = 'GET'
        rq_body = json.JSONEncoder().encode(json_str)
        res = self.req(method, rq_url, rq_body)
        LOG.info("Bandwidth Request Url: %s" % rq_url)
        LOG.info("Bandwidth status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("Bandwidth Body: %s" % rq_body)
        return res

    def req(self, method, rq_url, rq_body=''):
        rq_headers = {"Content-type": 'application/json',
                      'X-Auth-Token': self.token}
        try:
            httpClient = httplib.HTTPConnection(settings.API_SERVER)
            httpClient.request(method, rq_url, rq_body, rq_headers)
            response = httpClient.getresponse()
            return response
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            LOG.error('Could not connect to api_server %s' % e)
            return None


class MonthItem(object):
    def __init__(self, domain_name, max_value, max_time):
        self.domain_name = domain_name
        self.max_value = max_value
        self.max_time = max_time


# 合并流量、带宽数据
def mergeData(dataList):
    # 找到最长的元素
    import datetime
    import calendar
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    this_month_1 = datetime.datetime.now().strftime('%Y-%m-01 00:00')
    this_month_1_obj = datetime.datetime.strptime(this_month_1, "%Y-%m-%d %H:%M")
    days_count = calendar.monthrange(int(year), int(month))[1]  # 这个月的天数
    end_time = datetime.datetime.now().strftime('%Y-%m-' + str(days_count) + ' 23:55')
    end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    delta_5 = datetime.timedelta(seconds=300)

    time_list = []
    while this_month_1_obj <= end_time_obj:
        time_list.append(this_month_1_obj.strftime("%Y-%m-%d %H:%M"))
        this_month_1_obj += delta_5
    #lam = lambda x: datetime.datetime.now().strftime('%Y-%m-' + str(x)) \
    #    if (x > 9) else (datetime.datetime.now().strftime('%Y-%m-0' + str(x)))

    merged_data = []
    for key in time_list:
        item = {}
        sum = 0
        for j in dataList:
            value = float(j.get(key, 0))
            sum += value
        item["time"] = key
        item["value"] = str(sum)
        merged_data.append(item)
    values = [float(i["value"]) for i in merged_data]
    tmp = group(values, 288)
    max_lst = [max(item) for item in tmp]
    return max_lst


# 有一段数组，把它分成几个区间，取每个区间的最大值存到另一个数组里
def group(lst, n):
    num = len(lst) % n
    zipped = zip(*[iter(lst)] * n)
    return zipped if not num else zipped + [lst[-num:], ]