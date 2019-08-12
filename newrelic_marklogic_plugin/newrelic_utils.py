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
module responsible for updating NewRelic

docs for newrelic api - https://docs.newrelic.com/docs/apis

"""

import json
import logging
from newrelic_marklogic_plugin.__init__ import __version__
from newrelic_marklogic_plugin.http_utils import HTTPUtil

LOG = logging.getLogger(__name__)


class NewRelicUtility(object):
    """
    Upload metrics to New Relic
    """
    def __init__(self, host='localhost', pid='default', version=__version__):
        LOG.debug('init NewRelicUtility')
        self.host = host
        self.pid = pid
        self.version = version

    def update_newrelic(self, host=None, version=None, pid=None, name=None, guid=None, duration=None, metrics=None,
                        key=None, http_proxy=None, https_proxy=None):
        LOG.debug('update newrelic')

        # construct newrelic agent
        agent = {'host': host or self.host, 'pid': pid or self.pid, 'version': version or self.version}

        # construct newrelic components
        components = []
        component = {'name': name, 'guid': guid, 'duration': duration, 'metrics': metrics}
        components.append(component)

        # composite payload for sending to newrelic
        data = {'agent': agent, 'components': components}
        LOG.debug("payload:")
        LOG.debug(json.dumps(data))

        # send to the NewRelic API, supplying correct headers and using proxy (if defined).
        try:
            return HTTPUtil.http_post(
                scheme="https",
                url="https://platform-api.newrelic.com/platform/v1/metrics",
                headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'X-License-Key': key},
                payload=data,
                http_proxy=http_proxy,
                https_proxy=https_proxy)
        except Exception as exception:
            LOG.error("Problem accessing NewRelic Plugin API")
            LOG.error(exception)