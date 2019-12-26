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
plugin run script
"""

import getopt
import sys

import newrelic_marklogic_plugin


def init(args=None):
    """
    Extract options and initialize the New Relic plugin
    :return:
    """
    opts, args = getopt.getopt(args, 'hc:l:p:')

    pid_file = None
    log_file = None
    conf_file = None

    # extract options
    for opt, val in opts:
        if opt == '-h':
            newrelic_marklogic_plugin.RunPlugin.usage()
            sys.exit(0)
        elif opt == '-c':
            conf_file = val
        elif opt == '-l':
            log_file = val
        elif opt == '-p':
            pid_file = val
    return newrelic_marklogic_plugin.RunPlugin(confFile=conf_file, logFile=log_file, pidFile={pid_file})


if __name__ == "__main__":
    # start plugin run loop
    PLUGIN = init(sys.argv[1:])
    PLUGIN.run()
