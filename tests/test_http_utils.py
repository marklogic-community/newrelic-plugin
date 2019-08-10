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

# working directory=tests
import unittest
import logging
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from newrelic_marklogic_plugin.http_utils import HTTPUtil


LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
HOST = "node1"


class HTTPUtilTests(unittest.TestCase):
    def test_get_request_url(self):
        self.assertEqual("http://marklogic.com", HTTPUtil.get_request_url("http://marklogic.com"))

    def test_get_request_url_components(self):
        self.assertEqual("https://test.com:123/test", HTTPUtil.get_request_url(scheme="https", host="test.com", port=123, path="/test"))

    def test_get_request_url_combo(self):
        self.assertEqual("http://marklogic.com", HTTPUtil.get_request_url(url="http://marklogic.com", scheme="https", host="test.com", port=123, path="/test"))

    def test_get_auth_basic(self):
        auth = HTTPUtil.get_auth(auth="BASIC", user="basic-admin", passwd="basic-password")
        self.assertTrue(isinstance(auth, HTTPBasicAuth))
        self.assertEqual(auth.username, "basic-admin")
        self.assertEqual(auth.password, "basic-password")

    def test_get_auth_digest(self):
        auth = HTTPUtil.get_auth(auth="DIGEST", user="digest-admin", passwd="digest-password")
        self.assertTrue(isinstance(auth, HTTPDigestAuth))
        self.assertEqual(auth.username, "digest-admin")
        self.assertEqual(auth.password, "digest-password")

    def test_get_proxies(self):
        proxy = HTTPUtil.get_proxies(http_proxy="foo", https_proxy="bar")
        self.assertEqual(proxy.get("http"), "foo")
        self.assertEqual(proxy.get("https"), "bar")

    def test_get_proxies_http_only(self):
        proxy = HTTPUtil.get_proxies(http_proxy="foo")
        self.assertEqual(proxy.get("http"), "foo")
        self.assertIsNone(proxy.get("https", None))

    def test_get_proxies_https_only(self):
        proxy = HTTPUtil.get_proxies(https_proxy="foo")
        self.assertIsNone(proxy.get("http", None))
        self.assertEqual(proxy.get("https"), "foo")

    def test_get_proxies_none(self):
        self.assertIsNone(HTTPUtil.get_proxies())

    def test_get_auth_none(self):
        self.assertIsNone(HTTPUtil.get_auth())

    def test_http_get_status(self):
        response = HTTPUtil.http_get("http", HOST, 8002, "/manage/v2?view=status", "admin", "admin", "public", "DIGEST")
        self.assertTrue(isinstance(response, dict))
        self.assertIsNotNone(response["local-cluster-status"])

    def test_http_get_status_params(self):
        response = HTTPUtil.http_get(scheme="http", host=HOST, port=8002, path="/manage/v2?view=status", user="admin", passwd="admin", realm="public", auth="DIGEST")
        self.assertTrue(isinstance(response, dict))
        self.assertIsNotNone(response["local-cluster-status"])

    def test_http_get(self):
        response = HTTPUtil.http_get(url="http://www.google.com", headers={'Accept': 'text/html'}, format="html")
        # response will be HTML, not JSON
        self.assertFalse(isinstance(response, dict))

    def test_rest_post(self):
        response = HTTPUtil.http_post(scheme="https",
                                      url="https://platform-api.newrelic.com/platform/v1/metrics",
                                      headers={'Accept': 'application/json',
                                               'Content-Type': 'application/json',
                                               'X-License-Key': 'e8cf9b3d7aaca22a8632c7e01a14f8e722519b8a'},
                                      payload={
                                          "agent": {
                                              "host": HOST,
                                              "pid": 1234,
                                              "version": "1.0.0"
                                          },
                                          "components": [{
                                              "name": "marklogic_unittest",
                                              "guid": "com.marklogic",
                                              "duration": 60,
                                              "metrics": {
                                                  "Component/MarkLogic[UnitTest]": 50
                                              }
                                          }]
                                      })
        assert response
