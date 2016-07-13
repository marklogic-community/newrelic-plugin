newrelic\_marklogic
===================

`NewRelic <http://www.newrelic.com>`__ plugin for monitoring
MarkLogic.

Features
--------

-  Easy to install
-  Configurable selection of metrics
-  Retrieve summary metrics on local cluster, hosts, servers & forests.
-  Retrieve detail metrics on databases, forests, hosts, groups & servers.
-  Proxy access NewRelic api
-  Sample monitoring dashboards available at new relic plugin central.

Before you start
----------------

Minimally `Python 2.7.10  <https://www.python.org/>`__ installed.

Minimally `MarkLogic v7.0-6 <http://developer.marklogic.com/products>`__ installed
and running.

Require `NewRelic <http://www.newrelic.com/>`__ account.


Install, configure & run
------------------------

Install the plugin using any of the following methods.

- install from pypi repository

    ``pip install newrelic-marklogic-plugin``

- install direct from github

    ``pip install https://github.com/marklogic/newrelic-plugin/archive/master.zip``

- download `release <../../releases>`__  (or clone) repository and run the following.

    ``python setup.py install``


Next step is to create and edit configuration file.

1) Copy
   `etc/newrelic\_marklogic.conf.sample <etc/newrelic_marklogic.conf.sample>`__
   and rename to ``newrelic_marklogic.conf``

2) Edit ``newrelic_marklogic.conf`` ensuring correct MarkLogic
   connection details and NewRelic license key

Start reporting metrics to NewRelic by running the following.

    ``newrelic_marklogic.py -c newrelic_marklogic.conf``

Which will sample metrics every period of length duration as set within configuration.

You are free to start plugin as a background task, run via a scheduler (ex. cron job) or any other
environment specific approach.


Usage
-----

The configuration file drives most of the newrelic\_plugin features and
is split into several sections.

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

The 'newrelic' section specifies the NewRelic license key. Optionally you may nominate a proxy for accessing NewRelic Plugin API.

::

    [newrelic]

    # Your NewRelic license key.
    key = ****************************************

    # Proxy (ex. http://10.10.1.10:3128).
    http_proxy =

The 'plugin' section defines sample period for updating NewRelic, as well as the logging level for emitting messages about plugin operation.
There are a set of configurations for defining which statuses are captured by NewRelic.

- summary_status (True|False): retrieve local cluster summary status.
- databases (list of databases): retrieve database detailed status.
- hosts_summary_status (True|False):  retrieve summary of all hosts status.
- hosts (list of hosts): retrieve host detailed status.
- forests_summary_status (True|False): retrieve summary of all forests status.
- forests (list of forests): retrieve forest detailed status.
- groups (list of groups): retrieve group detailed status.
- servers_summary_status (True|False): retrieve summary of all servers status.
- servers (list of servers): retrieve server detailed status.

::

    [plugin]

    # NewRelic plugin display name.
    name = marklogic

    # Unique NewRelic plugin guid.
    guid = com.marklogic

    # Sample period in seconds.
    duration = 60

    # Set logging level (INFO|DEBUG|ERROR).
    log_level = DEBUG

    # Local cluster summary.
    summary_status= False

    # Database(s) detail status.
    databases= Documents

    # Hosts summary.
    hosts_summary_status= True

    # Host(s) detail status.
    hosts= 127.0.0.1

    # Forests summary.
    forests_summary_status= True

    # Forest(s) detail status.
    forests= Documents Meters

    # Group(s) detail status.
    groups= Default

    # Servers summary.
    servers_summary_status= True

    # Server(s) detail status (must supply group name ex. ServerName:GroupName).
    servers= Manage:Default

Issues, feature requests & contributing
---------------------------------------

Please file `bug reports <../../issues>`__, `feature
requests <../../issues>`__, and contribute with `pull
requests <../../pulls>`__ through GitHub.

License
-------

`Apache License v2.0 <LICENSE>`__
