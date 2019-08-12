#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2019 MarkLogic Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""
http utils dependent on requests module (https://github.com/kennethreitz/requests)

"""

import logging
import sys
import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth

LOG = logging.getLogger(__name__)


class HTTPUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def get_request_url(url=None, scheme=None, host=None, port=None, path=None):
        if url:
            requrl = url
        else:
            requrl = scheme + "://" + host + ":" + repr(port) + path
            LOG.debug(requrl)
        return requrl

    @staticmethod
    def get_auth(auth=None, user=None, passwd=None):
        if auth == "DIGEST":
            auth = HTTPDigestAuth(user, passwd)
        elif auth == "BASIC":
            auth = HTTPBasicAuth(user, passwd)
        else:
            auth = None
        return auth

    @staticmethod
    def get_proxies(http_proxy=None, https_proxy=None):
        proxies = None
        if http_proxy or https_proxy:
            proxies = {
                "http": http_proxy,
                "https": https_proxy
            }
        return proxies

    @staticmethod
    def http_get(scheme=None, host=None, port=None, path=None, user=None, passwd=None, realm=None, auth=None, url=None,
                 headers={'Accept': 'application/json'}, format="json", http_proxy=None, https_proxy=None):
        LOG.debug("dereference http GET")
        try:
            requrl = HTTPUtil.get_request_url(url, scheme, host, port, path)
            auth = HTTPUtil.get_auth(auth, user, passwd)
            proxies = HTTPUtil.get_proxies(http_proxy, https_proxy)
            response = requests.get(requrl, auth=auth, headers=headers, proxies=proxies)
            if response.status_code == 200:
                if format == "json":
                    return response.json()
                else:
                    LOG.error("Must dereference json representation.")
                    # return a response to aid testing http GET
                    return response
            else:
                LOG.error("HTTP Request returned %s when accessing %s, check configuration.", str(response.status_code), requrl)
                sys.exit(1)
            return
        except (requests.ConnectTimeout,
                requests.HTTPError,
                requests.ReadTimeout,
                requests.Timeout,
                requests.ConnectionError) as exception:
            LOG.error(exception)
        except requests.exceptions.RequestException as exception:
            LOG.error(exception)
            sys.exit(1)
        return

    @staticmethod
    def http_post(scheme=None, host=None, port=None, path=None, user=None, passwd=None, realm=None, auth=None, url=None,
                  headers={'Accept': 'application/json'}, format="json", payload=None, http_proxy=None, https_proxy=None):
        LOG.debug("execute http post call")
        try:
            requrl = HTTPUtil.get_request_url(url, scheme, host, port, path)
            auth = HTTPUtil.get_auth(auth, user, passwd)
            proxies = HTTPUtil.get_proxies(http_proxy, https_proxy)
            response = requests.post(requrl, json=payload, auth=auth, headers=headers, proxies=proxies)
            if format == "json":
                return response.json()
            else:
                return response.headers
        except (requests.ConnectTimeout,
                requests.HTTPError,
                requests.ReadTimeout,
                requests.Timeout,
                requests.ConnectionError) as exception:
            LOG.error(exception)
        except requests.exceptions.RequestException as exception:
            LOG.error(exception)
            sys.exit(1)
        return
