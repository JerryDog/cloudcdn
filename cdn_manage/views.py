# coding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from util.api_util import DomainApi, getTokenFromKS, MonthItem, mergeData
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from models import Domain, CacheRules, TaskList, DailyBandwidth
from django.conf import settings
import sys, json, re
import uuid
import logging
import datetime
import calendar
import traceback
from util import common_struct
from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf8')
# Create your views here.

LOG = logging.getLogger(__name__)

SUCCESS = '$(document).ready(function(){$("#succContent").html("%s");' \
          '$("#alertSucc").fadeIn();setTimeout("closeAlert(\'#alertSucc\')", 2000);});'

FAIL = '$(document).ready(function(){$("#failContent").html("%s");' \
       '$("#alertFail").fadeIn();setTimeout("closeAlert(\'#alertFail\')", 3000);});'

JS_DICT = {
    "succ_create": SUCCESS % "<strong>成功！</strong>添加域名成功",

    "succ_delete": SUCCESS % "<strong>成功！</strong>删除域名成功",

    "succ_update": SUCCESS % "<strong>成功！</strong>更新域名成功",

    "fail_create": FAIL % "<strong>错误！</strong>添加域名失败，原因：%s",

    "fail_update": FAIL % "<strong>错误！</strong>更新域名失败，原因：%s",
}


def index(req):
    if not req.session.has_key("project_id"):
        return HttpResponseRedirect('/login/')
    else:
        project_id = req.session['project_id']
    project_list = req.session['project_list']
    username = req.COOKIES.get('username')
    token = req.session.get('token')
    month_range = datetime.datetime.now().strftime('%Y年%m月01日') + ' - ' + \
                  datetime.datetime.now().strftime('%Y年%m月%d日')
    if username == settings.SUPERADMIN:
        domains = Domain.objects.using('api_db').exclude(domain_status='Delete')
    else:
        domains = Domain.objects.using('api_db').exclude(domain_status='Delete').filter(project_id=project_id)

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    days_count = calendar.monthrange(int(year), int(month))[1]
    #x_axis = map(lambda x: x.replace('-', '年').replace('=', '月') + '日', x_axis)
    #print x_axis
    if len(domains) == 0:
        all_domains = '--'
        max_bandwidth = '--'
        map_data = ['null' for i in range(1, days_count + 1)]
        return render_to_response('index.html', locals())
    else:
        all_domains = len(domains)

    domain_bandwidth = []
    for d in domains:
        single_domain_obj = DailyBandwidth.objects.using('api_db').filter(domain_name=d.domain_name).order_by("date")
        if single_domain_obj:
            max_value = max([float(j.bandwidth) for j in single_domain_obj])
            # 反推最大带宽出现的时间
            max_time = DailyBandwidth.objects.using('api_db')\
                .filter(domain_name=d.domain_name).filter(bandwidth=str(max_value))
            max_time = max_time[0].date
        else:
            max_value = '--'
            max_time = '--'
        domain_bandwidth.append(MonthItem(d.domain_name, max_value, max_time))

    return render_to_response('index.html', locals())


@csrf_exempt
def index_map(req):
    if req.method == "POST":
        if not req.session.has_key("project_id"):
            return HttpResponseRedirect('/login/')
        else:
            project_id = req.session['project_id']
        username = req.COOKIES.get('username')
        if username == settings.SUPERADMIN:
            #domains = Domain.objects.using('api_db').exclude(domain_status='Delete').all()
            domains = Domain.objects.using('api_db').filter(domain_status='Deployed')
        else:
            #domains = Domain.objects.using('api_db').exclude(domain_status='Delete').filter(project_id=project_id)
            domains = Domain.objects.using('api_db').filter(domain_status='Deployed').filter(project_id=project_id)
        # 只查状态是部署中的域名， InProgress 的不查
        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        lam = lambda x: datetime.datetime.now().strftime('%Y-%m-' + str(x)) \
            if (x > 9) else (datetime.datetime.now().strftime('%Y-%m-0' + str(x)))
        days_count = calendar.monthrange(int(year), int(month))[1]
        x_axis = [lam(i) for i in range(1, days_count + 1)]
        resp_json = {"xAxis": x_axis}
        domains_list = [n.domain_name for n in domains]
        try:
            data_to_merged = []
            for d in domains_list:
                item = {}
                bw_items = DailyBandwidth.objects.using('api_db').filter(domain_name=d).order_by("date")
                for bw in bw_items:
                    item[bw.date.strftime('%Y-%m-%d %H:%M')] = bw.bandwidth
                data_to_merged.append(item)
            bandwidth_list = mergeData(data_to_merged)
            #daily_max_list = [float(v["value"]) for v in bandwidth_list]
            map_data = bandwidth_list
            max_bandwidth = max(map(lambda x: float(x), bandwidth_list))
            resp_json["mapData"] = map_data
            resp_json["maxBandwidth"] = max_bandwidth
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            LOG.error('Get Index Flow Failed, %s' % e)
        return HttpResponse(json.dumps(resp_json), content_type="application/json")


@csrf_exempt
def login(req):
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        if username == settings.SUPERADMIN and password == settings.SUPERADMIN_PD:
            project_list = [["超级管理员", "1234567890"]]
            token = settings.ADMIN_TOKEN
        else:
            project_list, token = getTokenFromKS(username, password)
        if project_list and project_list != 'ConnError':
            LOG.info('User %s login!' % username)
            req.session['project_id'] = project_list[0][1]
            req.session['project_list'] = project_list
            req.session['token'] = token
            response = HttpResponseRedirect('/domain_manage/')
            response.set_cookie('username', username, settings.COOKIES_TIMEOUT)
            return response
        else:
            if project_list == 'ConnError':
                error = '链接超时'
                LOG.error('User %s login timeout!' % username)
            else:
                LOG.info('User %s login wrong password' % username)
                error = 'alert("用户名密码错误");'
            return render_to_response('new_login.html', locals())
    else:
        return render_to_response('new_login.html')


def logout(req):
    if req.COOKIES.get('username'):
        LOG.info('User %s logout!' % req.COOKIES.get('username'))
        response = HttpResponseRedirect('/login/')
        response.delete_cookie('username')
        return response
    else:
        return render_to_response('login.html')


@csrf_exempt
def switch_project(req):
    if req.method == "POST":
        new_project_id = req.POST.get('new_project_id')
        req.session['project_id'] = new_project_id
        return HttpResponse('1')


@csrf_exempt
def domain_manage(req):
    if req.method == "POST":
        if not req.session.has_key("session_id"):
            req.session['current_js'] = JS_DICT["fail_create"] % 'Null session_id'
            return HttpResponseRedirect('/domain_manage/')
        s_id = req.POST.get('session_id')
        if req.session["session_id"] != s_id:
            req.session['current_js'] = JS_DICT["fail_create"] % '请勿重复提交'
            return HttpResponseRedirect('/domain_manage/')
        else:
            del req.session["session_id"]
        cache_rules = req.POST.get('cache_rules', None)
        domain_name = req.POST.get('domain_name').strip()
        service_type = req.POST.get('service_type')
        ip_str = req.POST.get('ip_list').strip()
        test_url = req.POST.get('test_url').strip()
        project_id = req.session['project_id']
        username = req.COOKIES.get('username')
        token = req.session.get('token')
        try:
            api = DomainApi(token)
            domain = common_struct.Domain(domain_name=domain_name,
                                          origin_ips=ip_str.split('\r\n'),
                                          test_url=test_url,
                                          service_type=service_type,
                                          cache_behaviors=cache_rules)
            res = api.add(domain, project_id, username)
        except Exception, e:
            LOG.error('Create Domain Failed')
            req.session['current_js'] = JS_DICT["fail_create"] % e
            return HttpResponseRedirect('/domain_manage/')

        if res.status == 201:
            req.session['current_js'] = JS_DICT["succ_create"]
        else:
            req.session['current_js'] = JS_DICT["fail_create"] % json.loads(res.read()).get("error")
        return HttpResponseRedirect('/domain_manage/')
    else:
        if not req.session.has_key("project_id"):
            return HttpResponseRedirect('/login/')
        else:
            project_id = req.session['project_id']
        if req.session.has_key("current_js"):
            current_js = req.session.get('current_js')
            del req.session["current_js"]
        session_id = '%s' % uuid.uuid1()
        req.session['session_id'] = session_id
        username = req.COOKIES.get('username')
        if username == settings.SUPERADMIN:
            domains = Domain.objects.using('api_db').all()
        else:
            domains = Domain.objects.using('api_db').filter(project_id=project_id)
        project_list = req.session['project_list']
        return render_to_response('domain_manage.html', locals())


@csrf_exempt
def delete_domain(req):
    if req.method == 'POST':
        ids = req.POST.get('domain_ids')
        id_list = ids.split(',')
        username = req.COOKIES.get('username')
        token = req.session.get('token')
        api = DomainApi(token)
        for i in id_list:
            if i:
                id_obj = Domain.objects.using('api_db').filter(id=i)
                domain_name = id_obj[0].domain_name
                domain_id = id_obj[0].domain_id
                res = api.delete(domain_id)
                if res.status == 200:
                    LOG.info('User %s delete domain %s' % (username, domain_name))
                    print res.read()
                    result = 1
                else:
                    result = json.loads(res.read()).get("error")
        return HttpResponse(result)


@csrf_exempt
def edit_domain(req, domain_table_id):
    if req.method == 'POST':
        session_id = '%s' % uuid.uuid1()
        req.session['edit_session_id'] = session_id
        domain = Domain.objects.using('api_db').get(id=domain_table_id)
        ip_list = domain.ip_list.replace(',', '\r\n')
        try:
            domain_cache = CacheRules.objects.using('api_db').filter(domain_table_id=domain_table_id)
        except:
            domain_cache = ''
        return render_to_response('edit_domain_modal.html', locals(), context_instance=RequestContext(req))


@csrf_exempt
def update_domain(req, domain_table_id):
    if req.method == "POST":
        s_id = req.POST.get('edit_session_id')
        if not req.session.has_key("edit_session_id"):
            req.session['current_js'] = JS_DICT["fail_update"] % 'Null edit_session_id'
            return HttpResponseRedirect('/domain_manage/')
        if req.session["edit_session_id"] != s_id:
            req.session['current_js'] = JS_DICT["fail_update"] % '请勿重复提交'
            return HttpResponseRedirect('/domain_manage/')
        else:
            del req.session["edit_session_id"]
        cache_rules = req.POST.get('cache_rules', None)
        ip_str = req.POST.get('ip_list').strip()
        token = req.session.get('token')

        d = Domain.objects.using('api_db').get(id=domain_table_id)
        domain_name = d.domain_name
        test_url = d.test_url
        domain_id = d.domain_id
        service_type = d.domain_type
        try:
            api = DomainApi(token)
            domain = common_struct.Domain(domain_name=domain_name,
                                          origin_ips=ip_str.split('\r\n'),
                                          test_url=test_url,
                                          domain_id=domain_id,
                                          service_type=service_type,
                                          cache_behaviors=cache_rules)
            res = api.modify(domain)
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            LOG.error('Modify Domain Failed')
            req.session['current_js'] = JS_DICT["fail_update"] % e
            return HttpResponseRedirect('/domain_manage/')
        if res.status == 200:
            req.session['current_js'] = JS_DICT["succ_update"]
        else:
            req.session['current_js'] = JS_DICT["fail_update"] % json.loads(res.read()).get("error")
        session_id = '%s' % uuid.uuid1()
        req.session['edit_session_id'] = session_id
        return HttpResponseRedirect('/domain_manage/')


@csrf_exempt
def handler_cache(req):
    if req.method == 'POST':
        url = req.POST.get('url')
        url_type = req.POST.get('type')
        username = req.COOKIES.get('username')
        project_id = req.session['project_id']
        token = req.session.get('token')
        ############ 判断是否是当前项目下的域名###########
        pattern = re.compile('http:\/\/(.*?)\/')
        re_result = pattern.findall(url)
        if username == settings.SUPERADMIN:
            domains = Domain.objects.using('api_db').all().values_list('domain_name')
        else:
            domains = Domain.objects.using('api_db').filter(project_id=project_id).values_list('domain_name')
        this_domains = []
        for d in domains:
            this_domains.append(d[0])
        for r in re_result:
            if r not in this_domains:
                result = '请不要操作该项目以外的域名'
                return HttpResponse(result)
        #################################################
        api = DomainApi(token)
        urls_list = url.split('\n')
        if url_type == "0" or url_type == "1":
            # 0 是目录， 1是文件
            if url_type == "1":
                key = "urls"
            else:
                key = "dirs"
            json_str = {key: urls_list, "project_id": project_id, "username": username}
            res = api.purge(json_str)
        else:
            json_str = {"urls": urls_list, "project_id": project_id, "username": username}
            res = api.prefetch(json_str)

        if res.status == 200:
            result = '成功!'
        else:
            result = json.loads(res.read()).get("error")
        return HttpResponse(result)
    else:
        if not req.session.has_key("project_id"):
            return HttpResponseRedirect('/login/')
        else:
            project_id = req.session['project_id']
        username = req.COOKIES.get('username')
        if username == settings.SUPERADMIN:
            tasks = TaskList.objects.using('api_db').all()
        else:
            tasks = TaskList.objects.using('api_db').filter(project_id=project_id)
        for t in tasks:
            t.task_content = t.task_content.replace(',', '<br>')
        project_list = req.session['project_list']
        return render_to_response("refresh_cache.html", locals())


@csrf_exempt
def bandwidth(req):
    if req.method == 'POST':
        domain_name = req.POST.getlist('domain_name')
        start = req.POST.get('start')
        end = req.POST.get('end')
        project_id = req.session['project_id']
        token = req.session.get('token')
        api = DomainApi(token)
        json_str = {"domainName": ','.join(domain_name), "start": start, "end": end, "project_id": project_id}
        res = api.bandwidth(json_str)
        if res.status == 200:
            #random = uuid.uuid1()
            #path = settings.MONITOR_IMG % random
            #os.system('rm -f %s/*' % os.path.dirname(path))
            #with open(path, 'wb') as f:
            #    f.write(resp)
            return_json_str = json.loads(res.read())
            flow_list = return_json_str["bandwidth"]
            try:
                point_start = flow_list[0]['time']
                # point_start = '2015-12-04 14:35'
                point_start = [point_start[:4], point_start[5:7], point_start[8:10], point_start[11:13],
                               point_start[14:16]]
                point_start = [int(i) for i in point_start]
                data = []
                for i in flow_list:
                    data.append(float(i.get('value')))
                result = {"pointStart": point_start, "data": data}
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                LOG.error('Get Bandwidth Error, %s' % e)
                result = {"error": str(e) + ", 请联系管理员"}
        else:
            result = json.loads(res.read())
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        if not req.session.has_key("project_id"):
            return HttpResponseRedirect('/login/')
        else:
            project_id = req.session['project_id']
        username = req.COOKIES.get('username')
        if username == settings.SUPERADMIN:
            domains = Domain.objects.using('api_db').exclude(domain_status='Delete').all()
        else:
            domains = Domain.objects.using('api_db').exclude(domain_status='Delete').filter(project_id=project_id)
        project_list = req.session['project_list']
        return render_to_response("bandwidth.html", locals())


@csrf_exempt
def flow_value(req):
    if req.method == 'POST':
        domain_name = req.POST.getlist('domain_name')
        start = req.POST.get('start')
        end = req.POST.get('end')
        project_id = req.session['project_id']
        token = req.session.get('token')
        api = DomainApi(token)
        json_str = {"domainName": ','.join(domain_name), "start": start, "end": end, "project_id": project_id}
        res = api.flow(json_str)
        if res.status == 200:
            return_json_str = json.loads(res.read())
            flow_list = return_json_str["flowValue"]
            date = []
            flow = []
            for f in flow_list:
                date.append(f.get('time'))
                flow.append(f.get('value'))
            str = ','.join(date) + ';' + ','.join(flow)
            result = str
        else:
            result = json.loads(res.read()).get("error")
        return HttpResponse(result)
    else:
        if not req.session.has_key("project_id"):
            return HttpResponseRedirect('/login/')
        else:
            project_id = req.session['project_id']
        username = req.COOKIES.get('username')
        if username == settings.SUPERADMIN:
            domains = Domain.objects.using('api_db').exclude(domain_status='Delete').all()
        else:
            domains = Domain.objects.using('api_db').exclude(domain_status='Delete').filter(project_id=project_id)
        all_domains = ''
        for d in domains:
            all_domains = all_domains + ',' + d.domain_name
        project_list = req.session['project_list']
        return render_to_response("flow_value.html", locals())


def bandwidth_csv(req):
    if req.method == 'GET':
        import csv

        domain_name = req.GET.getlist('domain_name')
        start = req.GET.get('start')
        end = req.GET.get('end')
        project_id = req.session['project_id']
        token = req.session.get('token')
        api = DomainApi(token)
        json_str = {"domainName": ','.join(domain_name), "start": start, "end": end, "project_id": project_id}
        res = api.bandwidth(json_str)
        if res.status == 200:
            return_json_str = json.loads(res.read())
            flows = return_json_str["bandwidth"]
            response = HttpResponse(mimetype="text/csv")
            response['Content-Disposition'] = 'attachment; filename=%s_%s_bandwidth.csv' % (start, end)
            writer = csv.writer(response)
            writer.writerow(["Time", "BandWidth"])
            for f in flows:
                writer.writerow([f.get('time'), f.get('value')])
            return response
        else:
            result = json.loads(res.read()).get("error")
            return HttpResponse(result)
