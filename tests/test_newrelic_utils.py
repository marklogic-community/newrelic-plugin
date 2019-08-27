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

import unittest
import logging
import newrelic_marklogic_plugin
from newrelic_marklogic_plugin.newrelic_utils import NewRelicUtility

LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
HOST = "node1"

class NewRelicUtilsTests(unittest.TestCase):
    def test_init(self):
        utility = NewRelicUtility()
        self.assertEqual(utility.host, "localhost")
        self.assertEqual(utility.pid, "default")
        self.assertEqual(utility.version, newrelic_marklogic_plugin.__version__)

    @staticmethod
    def update(api_key):
        response = NewRelicUtility().update_newrelic(host=HOST,
                                                     pid=1234,
                                                     version="0.0.1",
                                                     name="marklogic_unittest",
                                                     guid="com.marklogic",
                                                     duration=60,
                                                     metrics={"Component/MarkLogic[UnitTest]": 100},
                                                     key=api_key)
        LOG.debug(response)
        return response

    # API_KEY is needed in order to test the New Relic API. Uncomment and add a key to test
    #def test_update(self):
    #    self.assertIsNotNone(self.update("ADD_YOUR_API_KEY_HERE"))
