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
from newrelic_marklogic_plugin.marklogic_status import MarkLogicStatus

LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
HOST = "localhost"
USER = "admin"
PASS = "admin"
AUTH = "DIGEST"
SCHEME = "http"
PORT = 8002


class MarkLogicUtilsTests(unittest.TestCase):

    def test_rest(self):
        status = MarkLogicStatus(scheme=SCHEME, user=USER, passwd=PASS, host=HOST, port=PORT, auth=AUTH, verify=False)
        response = status.get()
        LOG.debug(response)
        self.assertEqual(status.scheme, SCHEME)
        self.assertEqual(status.user, USER)
        self.assertEqual(status.passwd, PASS)
        self.assertEqual(status.host, HOST)
        self.assertEqual(status.port, PORT)
        self.assertEqual(status.auth, AUTH)
        self.assertTrue(isinstance(response, dict))
        self.assertIsNotNone(response["local-cluster-status"])

    def test_verify(self):
        status = MarkLogicStatus(scheme=SCHEME, user=USER, passwd=PASS, host=HOST, port=PORT, auth=AUTH)
        self.assertFalse(status.verify)
        status = MarkLogicStatus(scheme=SCHEME, user=USER, passwd=PASS, host=HOST, port=PORT, auth=AUTH, verify=False)
        self.assertFalse(status.verify)
        status = MarkLogicStatus(scheme=SCHEME, user=USER, passwd=PASS, host=HOST, port=PORT, auth=AUTH, verify=True)
        self.assertTrue(status.verify)
        status = MarkLogicStatus(scheme=SCHEME, user=USER, passwd=PASS, host=HOST, port=PORT, auth=AUTH, verify="/path/to/cacerts")
        self.assertEqual(status.verify, "/path/to/cacerts")

    def test_defaults(self):
        status = MarkLogicStatus()
        self.assertEqual(status.scheme, "http")
        self.assertEqual(status.host, None)
        self.assertEqual(status.user, None)
        self.assertEqual(status.passwd, None)
        self.assertEqual(status.port, 8002)
        self.assertEqual(status.auth, None)
        self.assertEqual(status.verify, False)
        self.assertEqual(status.url, None)

    def test_default_override(self):
        status = MarkLogicStatus(scheme="xcc", user="user", passwd="pass", port=123, host="host", auth="BASIC", verify=True)
        self.assertEqual(status.scheme, "xcc")
        self.assertEqual(status.port, 123)
        self.assertEqual(status.auth, "BASIC")
        self.assertEqual(status.verify, True)
        self.assertEqual(status.user, "user")
        self.assertEqual(status.passwd, "pass")
        self.assertEqual(status.host, "host")
