#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016 MarkLogic Corporation
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

opts, args = getopt.getopt(sys.argv[1:], 'hc:l:p')
pidfile = None
logfile = None
conffile = None

# extract options
for opt, val in opts:
    if opt == '-h':
        newrelic_marklogic_plugin.RunPlugin.usage()
        sys.exit(0)
    elif opt == '-c':
        conffile = val
    elif opt == '-l':
        logfile = val
    elif opt == '-p':
        pidfile = val

# start plugin run loop
plugin = newrelic_marklogic_plugin.RunPlugin(confFile=conffile, logFile=logfile, pidFile=pidfile)
plugin.run()
