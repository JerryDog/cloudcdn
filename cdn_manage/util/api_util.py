# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
import json
import logging

LOG = logging.getLogger(__name__)
import httplib
import traceback, sys
from django.conf import settings
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def getTokenFromKS(username, password):
    headers = {"Content-type": "application/json"}
    KEYSTONE = settings.KEYSTONE
    try:
        conn = httplib.HTTPConnection(KEYSTONE)
    except:
        return 'ConnError', 'ConnError'
    params = '{"auth": {"passwordCredentials": {"username": "%s", "password": "%s"}}}' % (username, password)
    try:
        conn.request("POST", "/v2.0/tokens", params, headers)
    except:
        return 'ConnError', 'ConnError'
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

    def analysis(self, json_str):
        rq_url = '/cdn_api/analysis'
        method = 'GET'
        rq_body = json.JSONEncoder().encode(json_str)
        res = self.req(method, rq_url, rq_body)
        LOG.info("Analysis Request Url: %s" % rq_url)
        LOG.info("Analysis status:%s, reason:%s" % (res.status, res.reason))
        LOG.info("Analysis Body: %s" % rq_body)
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
    # lam = lambda x: datetime.datetime.now().strftime('%Y-%m-' + str(x)) \
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


# 绘制验证码
# map:将str函数作用于后面序列的每一个元素
numbers = ''.join(map(str, range(10)))
chars = ''.join((numbers))
font_file = os.path.join(settings.BASE_DIR, 'cdn_manage/static/font/Arial.ttf') # choose a font file
def create_validate_code(size=(120, 30),
                         chars=chars,
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(255, 0, 0),
                         font_size=18,
                         font_type=font_file,
                         length=4,
                         draw_points=True,
                         point_chance=2):
    '''''
    size: 图片的大小，格式（宽，高），默认为(120, 30)
    chars: 允许的字符集合，格式字符串
    mode: 图片模式，默认为RGB
    bg_color: 背景颜色，默认为白色
    fg_color: 前景色，验证码字符颜色
    font_size: 验证码字体大小
    font_type: 验证码字体，默认为 Monaco.ttf
    length: 验证码字符个数
    draw_points: 是否画干扰点
    point_chance: 干扰点出现的概率，大小范围[0, 50]
    '''

    width, height = size
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        '''''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_points():
        '''''绘制干扰点'''
        chance = min(50, max(0, int(point_chance)))  # 大小限制在[0, 50]

        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''''绘制验证码字符'''
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 4),
                  strs, font=font, fill=fg_color)

        return strs

    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs
