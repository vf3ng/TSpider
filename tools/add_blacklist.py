#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2016/8/7 16:17
add blacklist domain or subdomain in runtime
"""
import sys

sys.path.append('../')
from core.utils.url import URL
from core.utils.redis_utils import RedisUtils

r = RedisUtils()
urls = []


def remove_from_tasklist(domain):
    # todo change to SIGNAL STRING in loop
    while True:
        try:
            urlstring = r.fetch_one_task(timeout=3)
            url = URL(urlstring)
            if r.is_blacklist_domain(url):
                continue
            urls.append(urlstring)
        except Exception as e:
            print str(e)
            break

    for url in urls:
        r.create_url_task(URL(url), set_target=False, valid_url_check=False)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: add_blacklist_domain.py blackdomain.com'
        sys.exit()
    domain = sys.argv[1]

    r.add_blacklist_domain(domain)
    if r.redis_task.hexists(r.h_domain_blacklist, domain):
        remove_from_tasklist(domain)
        print 'add success!'
    else:
        print 'add failed!'