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
HOST = "node1"


class MarkLogicUtilsTests(unittest.TestCase):
    def test_rest(self):
        status = MarkLogicStatus(scheme="http", user="admin", passwd="admin", host=HOST, port=8002, auth="DIGEST")
        response = status.get()
        LOG.debug(response)
        self.assertEqual(status.scheme, "http")
        self.assertEqual(status.user, "admin")
        self.assertEqual(status.passwd, "admin")
        self.assertEqual(status.host, HOST)
        self.assertEqual(status.port, 8002)
        self.assertEqual(status.auth, "DIGEST")
        self.assertTrue(isinstance(response, dict))
        self.assertIsNotNone(response["local-cluster-status"])