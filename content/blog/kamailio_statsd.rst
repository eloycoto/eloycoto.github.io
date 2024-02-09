Kamailio statsd explained
==========================

:date: 2015-03-16 16:00
:language: en-GB
:author: eloycoto
:head: Kamailio statsd best practices
:index_title: Kamailio statsd native integration.
:metatitle: Kamailio Statsd module explained
:tags: kamailio, graphite, statsd, grafana, statistics, monitoring
:metatags: kamailio, graphite, statsd, grafana
:description: Kamailio statsd help you to measure all the sip signalling here you have the best practices.
:keywords: Kamailio statsd, kamailio modules, graphite, grafana, statsd, gauges, counters

I remember when I heard about graphite/statsd. It was late of 2012 in the Python London Group. Few weeks before I read *Lean Startup* and I learnt to measure all the things to improve our business.

In early 2013 I started to use graphite. I tracked all logins, custom events, machine performance and all the running calls in the Foehn platform. After a few weeks I felt in love with Statsd/Graphite.

About Statsd/Graphite
---------------------

Graphite born to help all the developers to monitoring their Apps. The complete stack (Graphite/statsd/Grafana) is a opensource Application Performance Management (APM). This stack is an opensource alternative to NewRelic or datadog.

When we speak about graphite, we are speaking about 3 different projects:

**Graphite**: is a meta-package with the following components:

- Carbon: Is a daemon that listens for time-series data. UDP server with simple one direction protocol.
- Whisper: A simple database library for storing time-series data (Similar in design to RRD).
- Graphite Webapp: Django app that renders graphs on-demand.

**Statsd**: Statsd was born to fix Carbon weakness. Statsd is a wrapper that support `metric types <https://github.com/etsy/statsd/blob/master/docs/metric_types.md>`__. This wrapper makes graphite more powerful.

**Grafana**: previous projects are for store information. Grafana make the sexy part and it's a dashboard where the info can be shared.

Note: In the last year, a new event database is growing into the community. InfluxDB is more powerful than Graphite, supports different data types, and supports statsd protocol. Feel free to use with statsd_module. Community love it.

Why Statsd/Graphite
--------------------

Graphite stack helps developers to measure all the things. It's not a sql/no-sql database. It's a database designed to save realtime/events info, tools to aggregate the info after hours, days or years and finally provide an http rest API.

The main features of graphite are:
    - Save the info about events quickly. Only a simple key with value example: ('kamProd.gateways.gateway5').
    - Find with a quick look your keys in the graphite web app or grafana.
    - Compare information between days/hours.
    - Make graphs related with Phones, Web, gateways, custom apps, or whatever you want.
    - See trends in your platform in a simple panel.
    - Compare numbers, a lot of different numbers.

To deep more into graphite in this talk: `Video <http://vimeo.com/41146918>`__ and `Slides <https://docs.google.com/presentation/d/1QlLV00OyV-J8DkwfdUiXYRao-hLRkKFuu5DP90u1jKQ/edit?pli=1#slide=id.p>`__ or `in this blog post <https://codeascraft.com/2011/02/15/measure-anything-measure-everything/>`__.


Business Uses
-------------
Activating statsd module in kamailio could allow you to measure the following things:

- How many requests have been processed and how long each request took.
- The load of the gateways.
- How many invites have been received without proper number format.
- How many reinvites do you have in the application.
- Media Codec logging to make sure that always HD codec. :-)
- Test how long take a database query.
- Count how many invalid register do you have in the application.
- Count how many connections are using tls.

Those are only few examples. Whatever you want to measure, can be measured without any trouble.

.. image:: img/nice_dashboard.png
   :alt: Kamailio statsd native integration
   :align: center

Technical info
--------------

To enable statsd in Kamailio you need to add the module in the compile flags:

    .. code-block:: c

       make include_modules="statsd" cfg
       make install

Kamailio statsd only has 2 module parameters. `IP <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.p.serverIP>`__ and `Port <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.p.serverPort>`__.

Exported functions match with statsd metric types:

- **SET**: Simple info based on metric-value. `Kamailio module example <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.f.statsd_set>`__

- **Gauge**: Simple info too, but in this case if `flush interval <https://github.com/etsy/statsd/#key-concepts>`__ is not defined, statsd will send to graphite the last value. You can send +1 or -1 in the value field. `Kamailio module example <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.f.statsd_gauge>`__

- **Timming Options**: Timing is useful. Can be use `statsd_start <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.f.statsd_start>`__ and `statsd_stop <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.f.statsd_stop>`__ to track how long  took the code between start and stop.

- **Counting Options**: If you want to track decrements or increments `statsd_incr <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.f.statsd_incr>`__ and `statsd_decr <http://kamailio.org/docs/modules/devel/modules/statsd.html#statsd.f.statsd_decr>`__ and this match exactly with statsd counting definition.

    .. code-block:: c

        This is a simple counter. Add 1 to the "gorets" bucket. At each flush the current count is sent and reset to 0. If the count at flush is 0 then you can opt to send no metric at all for this counter, by setting config.deleteCounters (applies only to graphite backend). Statsd will send both the rate as well as the count at each flush.


Installing Graphite
--------------------

Install graphite is hard if you are not familiarized with python tools. My advice is to follow this `dockerfile <https://github.com/grafana/grafana-docker-dev-env>`__ and test it using docker. At the moment I'm running a system with more than 1700 metrics keys and it works perfectly.

Graphite/Statsd Environment
----------------------------

Environment is always important. Graphite environment is growing and it's important to add in this list:

- `CabotApp <http://cabotapp.com>`__: Monitor and alert system for your metrics. Gateway can be disabled if you are getting more than 100 5XX replies from it.
- `Diamond <https://github.com/BrightcoveOS/Diamond/wiki>`__: Python daemon that collects system metrics. `With a lot of useful collectors <https://github.com/BrightcoveOS/Diamond/wiki/Collectors>`__.

My advices
----------

- Use the docker image to start to test and production too!
- Grafana is a good friend, all your company will love it. `You must see this video <http://grafana.org/blog/2014/05/25/monitorama-video-and-update.html>`__
- Graphite query language is quite powerful, `have a look to the functions <http://graphite.readthedocs.org/en/1.0/functions.html>`__
- `TimeShift function <http://graphite.readthedocs.org/en/1.0/functions.html#graphite.render.functions.timeShift>`__ is one of the best functions in graphite.
- The learning curve of graphite is not easy. You can try with one metric and try every week to add a new graph in grafana.
