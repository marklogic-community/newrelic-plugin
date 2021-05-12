newrelic-marklogic-plugin is DEPRECATED
=========================

`New Relic Plugins are EOL <https://discuss.newrelic.com/t/new-relic-plugin-eol-wednesday-june-16th-2021/127267>`_ and have been deprecated in favor of `New Relic Integrations <https://docs.newrelic.com/docs/integrations/>`_. 

 On Wednesday, June 16th, 2021, New Relic will no longer support or maintain Plugins 192. Any plugin that is currently in use should be replaced by the New Relic Infrastructure agent 166. Along with support and maintenance, we will be removing access to the current plugin pages on the New Relic One platform.

The `New Relic Flex agent <https://github.com/newrelic/nri-flex>`_ is a recommended alternative to the newrelic-marklogic-plugin. There are `examples <https://github.com/newrelic/nri-flex/tree/master/examples>`_ of YAML files demonstrating how to leverage the New Relic Flex agent to retrieve MarkLogic Manage API statistics and send to New Relic, similar to how the newrelic-marklogic-plugin used to. 
 

`NewRelic <http://www.newrelic.com>`__ plugin for monitoring MarkLogic.
########

Features
--------

-  Easy to install
-  Configurable selection of metrics to retrieve
-  Retrieve summary metrics on local cluster, hosts, servers & forests
-  Retrieve detail metrics on databases, forests, hosts, groups & servers
-  Proxy access to NewRelic api
-  Sample monitoring dashboards available at `NewRelic plugin central <https://newrelic.com/plugins>`__.

Before you start
----------------

- Require minimally `Python 2.7.10  <https://www.python.org/>`__ installed
- `Requests python package <https://pypi.python.org/pypi/requests>`__ v2.11 or greater
- Require minimally `MarkLogic v7.0-6 <http://developer.marklogic.com/products>`__ installed and running
- Require `New Relic <http://www.newrelic.com/>`__ account

Docs
----

- `newrelic-marklogic-plugin docs on github <https://github.com/marklogic-community/newrelic-plugin>`__
- `newrelic-marklogic-plugin docs on pypi <https://pypi.python.org/pypi/newrelic-marklogic-plugin>`__

Install, configure & run
------------------------

Install the plugin using any of the following methods.

- install from pypi repository:

  ``pip install newrelic-marklogic-plugin``

- install direct from GitHub:

  ``pip install https://github.com/marklogic-community/newrelic-plugin/archive/master.zip``

- download `release <https://github.com/marklogic-community/newrelic-plugin/releases>`__  (or clone) repository and run the following:

  ``python setup.py install``


Next step is to create and edit configuration file.

1) Copy
   `etc/newrelic\_marklogic.conf.sample <https://github.com/marklogic-community/newrelic-plugin/blob/master/etc/newrelic_marklogic.conf.sample>`__
   and to ``newrelic_marklogic.conf``

2) Edit ``newrelic_marklogic.conf`` ensuring correct MarkLogic
   connection details and NewRelic license key

Start reporting metrics to NewRelic by running the following:

``newrelic_marklogic.py -c newrelic_marklogic.conf``

Which samples metrics every period of length duration as set within configuration.

It is recommended to initiate plugin as a background task, run via a scheduler (ex. cron job) or using any other
approach appropriate for your environment.

Running with -h flag will emit usage instructions for running plugin:

``newrelic_marklogic.py -h``

::

    usage: ./newrelic_marklogic.py [-h] [-c config file] [-l log file]

    -h print usage instructions  (this message)
    -c config file               (default: newrelic_marklogic.conf)
    -l log file                  (default: newrelic_marklogic.log)

Usage
-----

The configuration file drives all newrelic-marklogic-plugin features and is split into several sections.

The 'marklogic' section contains connection details to MarkLogic server and Management REST API.

::

    [marklogic]

    # Scheme to use when accessing MarkLogic management REST API (http|https).
    scheme = http

    # Host to use when accessing MarkLogic management REST API (FQDN hostname).
    host = localhost

    # Port to use when accessing MarkLogic management REST API.
    port = 8002

    # Authentication to use when accessing MarkLogic management REST API (BASIC|DIGEST).
    auth= DIGEST

    # Username to use when accessing MarkLogic management REST API.
    user = admin

    # Password to use when accessing MarkLogic management REST API.
    pass = admin

    # (optional) Either a boolean, in which case it controls whether we verify
    # the server's TLS certificate, or a string, in which case it must be a path
    # to a CA bundle to use. Defaults to ``False``.
    verify = False

The 'newrelic' section specifies the New Relic license key. Optionally you may nominate a proxy for accessing the New Relic Plugin API.

::

    [newrelic]

    # Your NewRelic license key.
    key = ****************************************

    # Proxy (ex. http://10.10.1.10:3128).
    http_proxy =

The 'plugin' section defines sample period for updating New Relic, as well as the logging level for emitting messages about plugin operation.

There are a set of configurations for defining which statuses are captured by New Relic, summarized below.

- **summary_status** (True|False): retrieve local cluster summary status.
- **databases** (list of databases): retrieve database detailed status.
- **hosts_summary_status** (True|False):  retrieve summary of all hosts status.
- **hosts** (list of hosts): retrieve host detailed status.
- **forests_summary_status** (True|False): retrieve summary of all forests status.
- **forests** (list of forests): retrieve forest detailed status.
- **groups** (list of groups): retrieve group detailed status.
- **servers_summary_status** (True|False): retrieve summary of all servers status.
- **servers** (list of servers): retrieve server detailed status.

::

    [plugin]

    # New Relic plugin display name.
    name = myMarkLogicServer

    # Unique New Relic plugin guid.
    guid = com.marklogic

    # Sample period in seconds.
    duration = 60

    # Set logging level (INFO|DEBUG|ERROR).
    log_level = DEBUG

    # Local cluster summary.
    summary_status = False

    # Database(s) detail status.
    databases = Documents

    # Hosts summary.
    hosts_summary_status = True

    # Host(s) detail status.
    hosts = 127.0.0.1

    # Forests summary.
    forests_summary_status = True

    # Forest(s) detail status.
    forests = Documents Meters

    # Group(s) detail status.
    groups = Default

    # Servers summary.
    servers_summary_status = True

    # Server(s) detail status (must supply group name ex. ServerName:GroupName).
    servers = Manage:Default

Create pypi distribution
---------------------------------------

1. To create an official distribution, first ensure that all tests are passing:

   ``python -m unittest discover -s tests``

2. bump version number and create a distro:

   ``python setup.py sdist``

3. Upload the package to pypitest:

   ``twine upload --repository-url https://test.pypi.org/legacy/ dist/*``

4. after verifying all is well, generate the distro on pypi:

   ``twine upload dist/*``

Issues, feature requests & contributing
---------------------------------------

Please file `bug reports <https://github.com/marklogic-community/newrelic-plugin/issues>`__, `feature
requests <https://github.com/marklogic-community/newrelic-plugin/issues>`__, and contribute with `pull
requests <https://github.com/marklogic-community/newrelic-plugin/pulls>`__ through GitHub.

Copyright & License
-------------------

newrelic-marklogic-plugin Copyright 2019 MarkLogic Corporation

newrelic-marklogic-plugin is licensed under the Apache License, Version 2.0 (the "License"). A copy of the license is included within this package.

`Apache License v2.0 <https://github.com/marklogic-community/newrelic-plugin/blob/master/LICENSE>`__
