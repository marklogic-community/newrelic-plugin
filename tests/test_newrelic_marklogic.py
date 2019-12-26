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
import sys

sys.path.append('./scripts')
import newrelic_marklogic


class NewRelicMarkLogicTest(unittest.TestCase):

    def test_init(self):
        plugin = newrelic_marklogic.init(["-c", "etc/newrelic_marklogic.conf.sample", "-l", "test.log", "-p", "test.pid"])
        self.assertEqual(str(plugin.logFile), "test.log")
        self.assertEqual(str(plugin.confFile), "etc/newrelic_marklogic.conf.sample")
        self.assertTrue("test.pid" in plugin.pidfile_path)
        self.assertFalse(plugin.ml_verify)
