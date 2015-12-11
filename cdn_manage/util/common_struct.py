# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
class Domain(object):
    '''表示为域名对象'''
    def __init__(self, domain_name=None, service_type=None, test_url=None, enabled=None,
                 domain_id=None, comment=None, origin_ips=None, cache_behaviors=None):
        self.domain_name = domain_name
        self.service_type = service_type
        self.enabled = enabled
        self.test_url = test_url
        self.domain_id = domain_id
        self.comment = comment
        self.origin_ips = origin_ips
        self.cache_behaviors = cache_behaviors