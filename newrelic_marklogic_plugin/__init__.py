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
__init__.py module entry point for running plugin

"""

import json
import re
import sys
import time
import logging
import ConfigParser  # TBD- python 3.5 does not have this module

import newrelic_marklogic_plugin.newrelic_utils
from newrelic_marklogic_plugin.marklogic_status import MarkLogicStatus

__version__ = '0.2.9'


DECL = {
    'pidFile': 'newrelic_marklogic.pid',
    'logFile': 'newrelic_marklogic.log',
    'confFile': 'newrelic_marklogic.conf',
    'logLevel': logging.INFO
}

LOG = logging.getLogger(__name__)


class RunPlugin(object):
    def __init__(self, pidFile=None, logFile=None, confFile=None):

        # setup configuration
        self.confFile = confFile or DECL['confFile']
        try:
            LOG.debug('parse config')
            config = ConfigParser.ConfigParser()
            config.read(self.confFile)

            self.ml_host = config.get('marklogic', 'host')
            self.ml_port = config.getint('marklogic', 'port')
            self.ml_url = "http://" + self.ml_host + ":"
            self.ml_url += repr(self.ml_port)
            LOG.debug(self.ml_url)
            self.ml_user = config.get('marklogic', 'user')
            self.ml_pass = config.get('marklogic', 'pass')
            self.ml_scheme = config.get('marklogic', 'scheme')
            self.ml_auth = config.get('marklogic', 'auth')
            self.nr_license_key = config.get('newrelic', 'key')
            self.nr_http_proxy = config.get('newrelic', 'http_proxy')
            self.nr_https_proxy = config.get('newrelic', 'https_proxy')
            self.plugin_name = config.get('plugin', 'name')
            self.plugin_guid = config.get('plugin', 'guid')
            self.plugin_duration = config.getint('plugin', 'duration')
            self.plugin_summary_status = config.getboolean('plugin', 'summary_status')
            self.plugin_databases = config.get('plugin', 'databases')
            self.plugin_hosts_summary_status = config.getboolean('plugin', 'hosts_summary_status')
            self.plugin_hosts = config.get('plugin', 'hosts')
            self.plugin_forests_summary_status = config.getboolean('plugin', 'forests_summary_status')
            self.plugin_forests = config.get('plugin', 'forests')
            self.plugin_groups = config.get('plugin', 'groups')
            self.plugin_servers_summary_status = config.getboolean('plugin', 'servers_summary_status')
            self.plugin_servers = config.get('plugin', 'servers')

            # setup logging
            self.logFile = logFile or DECL['logFile']
            self.log_level = config.get('plugin', 'log_level') or DECL["logLevel"]
            handler = logging.FileHandler(self.logFile, 'w')
            formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            LOG.addHandler(handler)
            LOG.setLevel(self.log_level)
            LOG.debug("init plugin")
            stream_handler = logging.StreamHandler(sys.stderr)
            LOG.addHandler(stream_handler)

            # setup pid
            self.pidfile_path = pidFile or DECL['pidFile']
            self.pidfile_timeout = 5

        except ConfigParser.ParsingError as error:
            LOG.error("Problem with configuration.")
            LOG.error(error)

    def run(self):
        LOG.info("newrelic_marklogic plugin now sending statuses to NewRelic Plugin API (to see more log messages change log_level=DEBUG).")
        while True:
            try:
                self.statusUpdate()
            except Exception as exception:
                LOG.error(exception)
            time.sleep(self.plugin_duration)

    def statusUpdate(self):
        """
        Retrieve MarkLogic status information and post to New Relic
        :return:
        """
        LOG.debug("retrieve statuses and update newrelic")
        status = MarkLogicStatus(scheme=self.ml_scheme, user=self.ml_user, passwd=self.ml_pass, auth=self.ml_auth, host=self.ml_host, port=self.ml_port)
        metrics = {}
        # retrieve summary status
        if self.plugin_summary_status:
            metrics.update(self.get_summary_status(status))

        # retrieve forest summary status
        if self.plugin_forests_summary_status:
            metrics.update(self.get_resource_summary_status(status, "forests"))

        # retrieve host summary status
        if self.plugin_hosts_summary_status:
            metrics.update(self.get_resource_summary_status(status, "hosts"))

        # retrieve server summary status
        if self.plugin_servers_summary_status:
            metrics.update(self.get_resource_summary_status(status, "servers"))

        # retrieve specific database detail status
        if self.plugin_databases:
            metrics.update(self.get_database_detail_status(status, self.plugin_databases))

        # retrieve specific host detail status
        if self.plugin_hosts:
            metrics.update(self.get_host_detail_status(status, self.plugin_hosts))

        # retrieve specific forest detail status
        if self.plugin_forests:
            metrics.update(self.get_forest_detail_status(status, self.plugin_forests))

        # retrieve specific group detail status
        if self.plugin_groups:
            metrics.update(self.get_group_detail_status(status, self.plugin_groups))

        # retrieve specific server detail status
        if self.plugin_servers:
            metrics.update(self.get_server_detail_status(status, self.plugin_servers))

        update_newrelic = newrelic_utils.NewRelicUtility().update_newrelic(host=self.ml_host,
                                                                           pid=1,
                                                                           version=__version__,
                                                                           name=self.plugin_name,
                                                                           guid=self.plugin_guid,
                                                                           duration=self.plugin_duration,
                                                                           metrics=metrics,
                                                                           key=self.nr_license_key,
                                                                           http_proxy=self.nr_http_proxy,
                                                                           https_proxy=self.nr_https_proxy)

        if "error" in update_newrelic:
            LOG.error(update_newrelic["error"])
        else:
            LOG.debug("update status: %s", json.dumps(update_newrelic))

    @classmethod
    def get_summary_status(cls, status):
        """
        Retrieve the cluster status and return a dict with summary metrics
        :param status:
        :return:
        """
        metrics = {}
        LOG.debug("Retrieving cluster status")
        cluster_status = status.get()
        status_relations = cluster_status['local-cluster-status']['status-relations']
        for relation in status_relations:
            status_relation = status_relations[relation]
            prefix = "Component/" + status_relation["typeref"] + "/"
            summary_obj = status_relation[relation + "-summary"]
            for key in summary_obj:
                cls.process_metric(metrics, prefix, summary_obj, key)
        return metrics

    @classmethod
    def get_resource_summary_status(cls, status, resource):
        """
        Retrieve the summary status for the given resource and return a dict with the parsed metrics
        :param status:
        :param resource:
        :return:
        """
        metrics = {}
        LOG.debug("Retrieving resource %s", resource)
        resource_status = status.get(resource=resource)

        prefix = "Component/" + resource + "/"
        for status_key in resource_status:
            if status_key.endswith("-status-list"):
                properties = resource_status[status_key]["status-list-summary"]
                for key in properties:
                    cls.process_metric(metrics, prefix, properties, key)
        return metrics

    @classmethod
    def get_database_detail_status(cls, status, databases):
        return cls.get_resource_detail_status(status, "databases", databases)

    @classmethod
    def get_host_detail_status(cls, status, hosts):
        return cls.get_resource_detail_status(status, "hosts", hosts)

    @classmethod
    def get_forest_detail_status(cls, status, forests):
        return cls.get_resource_detail_status(status, "forests", forests)

    @classmethod
    def get_group_detail_status(cls, status, groups):
        return cls.get_resource_detail_status(status, "groups", groups)

    @classmethod
    def get_server_detail_status(cls, status, servers):
        """
        Retrieve the status for each of the space separated server:group (colon separated) combinations and return a
        dict with the parsed metrics
        :param status:
        :param servers:
        :return:
        """
        metrics = {}
        for server_group in re.split(" ", servers):
            server_group_tuple = server_group.split(":")
            if len(server_group_tuple) == 2:
                server, group = server_group_tuple
                LOG.debug("Requesting server details for name: " + server + " group: " + group)
                server_status = status.get(resource="servers", name=server, group=group)
                prefix = "Component/servers/" + server + "/"
                metrics.update(cls.process_status(prefix, server_status))
            else:
                LOG.error("cannot retrieve %s server status, check configuration", server_group)
        return metrics

    @classmethod
    def get_resource_detail_status(cls, status, resource_type, resource_names):
        """
        Retrieve the resource for each of the (space separated) resource names and return a dict with the parsed metrics
        :param status:
        :param resource_type:
        :param resource_names:
        :return:
        """
        metrics = {}
        for name in re.split(" ", resource_names):
            LOG.debug("Retrieving " + resource_type + ": " + name)
            resource_status = status.get(resource=resource_type, name=name)
            prefix = "Component/" + resource_type + "/" + name + "/"
            metrics.update(cls.process_status(prefix, resource_status))
        return metrics

    @classmethod
    def process_status(cls, prefix, status_obj):
        """
        Process the status response and return a dict with each of the status-properties children
        :param prefix:
        :param status_obj:
        :return:
        """
        metrics = {}
        for status_key, status in status_obj.items():
            if status_key.endswith("-status") and isinstance(status, dict):
                properties = status["status-properties"]
                for key in properties:
                    cls.process_metric(metrics, prefix, properties, key)
        return metrics

    @staticmethod
    def label_units(obj, metric):
        """
        Returns the label, conditionally with a metric suffix if units are specified
        :param obj:
        :param metric:
        :return:
        """
        label = metric
        if isinstance(obj[metric], dict):
            units = obj[metric].get("units", "")
            # ensure that it isn't blank
            if units.strip():
                label += "[" + units + "]"
        return label

    @classmethod
    def set_metric(cls, metrics, prefix, obj, key):
        """
        Add a metric for the property specified
        :param metrics:
        :param prefix:
        :param obj:
        :param key:
        :return:
        """
        value = obj[key]
        if isinstance(value, dict):
            value = value.get("value")
        LOG.debug(str(key) + "=" + str(value))
        metrics[prefix + cls.label_units(obj, key)] = value

    @classmethod
    def process_metric(cls, metrics, prefix, obj, prop,
                       ignore_pattern="backup-job|.*-cache-partition$|database-replication-status|error-handler" \
                                      "|license-key-option|local-disk-failover|output-encoding|root$" \
                                      "|shared-disk-failover|stand$|url-rewriter"):
        """
        Evaluate whether the property in the given object should be skipped, added to metrics dic,
        or continue walking the object
        :param metrics:
        :param prefix:
        :param obj:
        :param prop:
        :param ignore_pattern:
        :return:
        """
        if ignore_pattern and re.match(ignore_pattern, prop):
            LOG.debug("ignoring: %s", prop)
        else:
            value = obj[prop]
            if isinstance(value, dict):
                if prop.endswith("-status-summary"):
                    metric = prop[:prop.index("-status-summary")]
                    metric_prefix = prefix + metric + "/"
                    for key in value:
                        cls.process_metric(metrics, metric_prefix, value, key)
                elif prop.endswith("-properties"):
                    metric = prop[:prop.index("-properties")]
                    metric_prefix = prefix + metric + "/"
                    for key in value:
                        cls.process_metric(metrics, metric_prefix, value, key)
                elif prop.endswith("-detail"):
                    property_prefix = prefix
                    if prop != "status-detail":
                        property_prefix += "detail/"
                    for detail in value:
                        cls.process_metric(metrics, property_prefix, value, detail)
                elif value.get("units", "") == "bool":
                    LOG.debug("ignoring: %s", prop)
                else:
                    cls.set_metric(metrics, prefix, obj, prop)
            else:
                cls.set_metric(metrics, prefix, obj, prop)

    @staticmethod
    def singular(value):
        """
        Remove trailing "s" from the given string value and return
        """
        if value.endswith('s'):
            return value[:-1]
        return value

    @staticmethod
    def usage():
        LOG.debug("output usage instructions")
        print("""newrelic_marklogic v%s - NewRelic plugin for monitoring MarkLogic.

usage: ./newrelic_marklogic.py [-h] [-c config file] [-l log file]

    -h print usage instructions  (this message)
    -c config file               (default: %s)
    -l log file                  (default: %s)
    """ % (__version__,
           DECL['confFile'],
           DECL['logFile']))
