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
import logging, sys
try:
    from StringIO import StringIO
except ImportError:
    # Python2
    from io import StringIO

import newrelic_marklogic_plugin
from newrelic_marklogic_plugin.marklogic_status import MarkLogicStatus

LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class PluginTests(unittest.TestCase):
    nrml = newrelic_marklogic_plugin.RunPlugin(logFile='newrelic_marklogic_plugin.log',
                                               confFile='etc/newrelic_marklogic.conf.sample')

    def test_version(self):
        assert newrelic_marklogic_plugin.__version__ == "0.2.9"

    def test_RunPlugin(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.nrml.statusUpdate()
        self.assertEqual(sys.stdout.getvalue().strip(), '')

    def test_ConfigFile(self):
        self.nrml.statusUpdate()
        self.assertEqual(self.nrml.ml_user, "admin")
        self.assertEqual(self.nrml.ml_pass, "admin")

    def test_usage(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        newrelic_marklogic_plugin.RunPlugin.usage()
        self.assertEqual(sys.stdout.getvalue().strip(),
                         'newrelic_marklogic v' + newrelic_marklogic_plugin.__version__ + ' - NewRelic plugin for monitoring MarkLogic.\n\n' \
                         'usage: ./newrelic_marklogic.py [-h] [-c config file] [-l log file]\n\n' \
                         '    -h print usage instructions  (this message)\n' \
                         '    -c config file               (default: newrelic_marklogic.conf)\n' \
                         '    -l log file                  (default: newrelic_marklogic.log)')

    def test_label_units(self):
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.label_units({"foo": "bar"}, "foo"), "foo")
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.label_units({"foo": {"units": "MB/sec", "value": 5}}, "foo"), "foo[MB/sec]")
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.label_units({"foo": {"units": "", "value": 5}}, "foo"), "foo")
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.label_units({"foo": {"units": "     ", "value": 5}}, "foo"), "foo")
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.label_units({"foo": {"value": 5}}, "foo"), "foo")

    def test_singular(self):
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.singular("forests"), "forest")
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.singular("forest"), "forest")
        self.assertEqual(newrelic_marklogic_plugin.RunPlugin.singular(""), "")

    def test_set_metric(self):
        metrics = {}
        response = {
            "large-write-rate": {"units": "MB/sec", "value": 1.234},
            "memory-process-rss":233
        }
        newrelic_marklogic_plugin.RunPlugin.set_metric(metrics, "Component/forests/", response, "large-write-rate")
        newrelic_marklogic_plugin.RunPlugin.set_metric(metrics, "Component/hosts/", response, "memory-process-rss")
        self.assertEqual(metrics["Component/forests/large-write-rate[MB/sec]"], 1.234)
        self.assertEqual(metrics["Component/hosts/memory-process-rss"], 233)

    def test_process_metric(self):
        metrics = {}
        prefix = "Component/test/"
        response = {
            "root": "this value should be ignored",
            "enabled" : {"units": "bool", "value": True},
            "hosts-status-summary" : {"foo": 1, "memory-process-rss": 10},
            "foo-properties": {"bar": {"units": "quantity", "value": 22}},
            "bar-detail": {"baz": {"units": "quantity", "value": 33}},
            "status-detail": {"bat": {"units": "quantity", "value": 44}},
            "memory-process-rss": 35,
            "xyz": 99
        }

        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "root")
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "enabled")
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "hosts-status-summary")
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "foo-properties")
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "bar-detail")
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "status-detail")

        self.assertTrue("Component/test/root" not in metrics)
        self.assertTrue("Component/test/enabled" not in metrics)
        self.assertEqual(metrics.get("Component/test/hosts/foo"), 1)
        self.assertEqual(metrics.get("Component/test/hosts/memory-process-rss"), 10)
        self.assertEqual(metrics.get("Component/test/foo/bar[quantity]"), 22)
        self.assertEqual(metrics.get("Component/test/detail/baz[quantity]"), 33)
        self.assertEqual(metrics.get("Component/test/bat[quantity]"), 44)
        self.assertTrue("Component/test/detail/bat[quantity]" not in metrics)

        # custom exclude pattern can be used
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "xyz", "xyz")
        self.assertTrue("Component/test/xyz" not in metrics)
        # when not applied, the field is added
        newrelic_marklogic_plugin.RunPlugin.process_metric(metrics, prefix, response, "xyz")
        self.assertEqual(metrics.get("Component/test/xyz"), 99)

    def test_process_status(self):
        status_obj = {
            "server-status": {"status-properties": {"foo": {"units": "quantity", "value": 1}, "bar": 2},
                              "status-extra-properties": {"foo2": {"units": "quantity", "value": 3}, "bar2": 4}
                             },
            "server-extra-status": "should be ignored"
        }
        prefix = "Component/test/"
        payload = self.nrml.process_status(prefix, status_obj)
        self.assertEqual(len(payload.keys()), 2)
        self.assertEqual(payload.get("Component/test/foo[quantity]"), 1)
        self.assertEqual(payload.get("Component/test/bar"), 2)

    def test_get_summary_status(self):
        status = MarkLogicStatus(scheme=self.nrml.ml_scheme, user=self.nrml.ml_user, passwd=self.nrml.ml_pass, auth=self.nrml.ml_auth, host=self.nrml.ml_host, port=self.nrml.ml_port)
        payload = self.nrml.get_summary_status(status)
        LOG.debug(payload)
        self.assertGreater(len(payload.keys()), 0)

    def test_get_server_detail_status(self):
        status = MarkLogicStatus(scheme="http", user="admin", passwd="admin", port=8002, host="localhost", auth="DIGEST")
        metrics = self.nrml.get_server_detail_status(status, "nocolon")
        self.assertFalse(metrics)
        metrics = self.nrml.get_server_detail_status(status, "Manage:Default")
        self.assertTrue(metrics)

    def test_verify(self):
        self.assertFalse(self.nrml.ml_verify)
