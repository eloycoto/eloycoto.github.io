Kamailio statsd, better statistics in your voip platform.
============================================================

:date: 2014-10-22 16:00
:language: en-GB
:head: Kamailio integration with Statsd and Graphite.
:author: eloycoto
:index_title: Kamailio statsd native integration.
:metatitle: How to integrate kamailio with Graphite using kamailio statsd
:tags: kamailio, graphite, statsd, grafana, statistics, monitoring
:metatags: kamailio, graphite, statsd, grafana
:description: Kamailio statsd is a module to integrate your Voip platform with Realtime graphing Graphite. You can get better statistics with this module.
:keywords: kamailio statsd, kamailio modules, graphite, grafana, statsd, gauges, counters

I remember when I read about `Graphite <http://graphite.wikidot.com/>`__. I was reading that Vimeo used it for making realtime monitoring in their projects and reporting for all the team. I got a chance to test with my local apps and after a few days I started to love graphite.

I start to use graphite in my web apps. After few weeks I needed to monitor a new feature deployed in one of our kamailio. The first time I used mod_python+statsd, but I realise that using python module was not the best way so I write `statsd module <https://github.com/eloycoto/statsd>`__ that work native with kamailio.

`I made this module, after 7 years working with Kamailio <https://github.com/eloycoto/statsd>`__, I read/modified a lot of modules, but I never had a chance to write a new one.

Kamailio mod statsd provides just four functions. All of those functions are damn easy to understand but if you are not familiarized with this world, I would recommend you to check this posts:

    - `Introduction to graphite and collectd <https://www.digitalocean.com/community/tutorials/an-introduction-to-tracking-statistics-with-graphite-statsd-and-collectd>`__
    - `Undertanding graphite and statsd <http://blog.pkhamre.com/2012/07/24/understanding-statsd-and-graphite/>`__
    - `Statsd metric types <https://github.com/etsy/statsd/blob/master/docs/metric_types.md>`__

.. image:: img/grafana1.png
   :alt: grafana kamailio integration
   :align: center

If you want to test the module without a lot of trouble, the recommended way in my opinion is to use this `Docker deploy <https://github.com/grafana/grafana-docker-dev-env>`__ (Grafana is the best dashboard for graphite).

And after have it installed, go throught the `READAME.md <https://github.com/eloycoto/statsd/blob/master/Readme.md>`__ file:

`Kamailio statsd parameters <http://github.com/eloycoto/kamailio-statsd>`__:
-------------------------------------------------------------------------------------------------------

**IP**: Statsd listen IP.
    .. code-block:: c

        modparam("statsd", "ip", "127.0.0.1")

**PORT**: Statsd listen port.
    .. code-block:: c

        modparam("statsd", "port", "8125")


`Kamailio statsd functions <http://github.com/eloycoto/kamailio-statsd>`__:
---------------------------------------------------------------------------------------------------

**Set**:  counting unique occurrences of events between flushes, using a Set to store all occurring events.
    .. code-block:: c

        route [customer_credit]{
            statsd_set(“customer."+$avp(customer)+”credit”, $var(credit))
        }

**Gauge**:  A gauge simply indicates an arbitrary value at a point in time. You can use like this:

    .. code-block:: c

        route [gauge_method]{
                statsd_gauge("method.count"+$rm, “1”);
                if($avp(s:prepaid)) statsd_gauge("customer.prepaid", “+1”);
        }


**Timing**: You can use timing options in any function, or specific route, with code like this:

    .. code-block:: c

        route [long_mysql_query]{
                statsd_start("long_mysql_query");
                sql_query("ca", "select sleep(rand()/4)", "ra");
                statsd_stop("long_mysql_query");
        }

Timers (statsd_start, statsd_stop) are an incredibly powerful tool for tracking application performance.


**Counters**:  You can use statsd_incr or statsd_decr for increment/decrement a counter. For example I used a lot the counter with GeoIP module or log any specific feature in the platform (Prepaid user, new features launch).

    .. code-block:: c

        route[country]{
            if(geoip_match("$si", "src")){
                   statsd_incr("country."+$(gip(src=>cc)));
            }
        }

You can also check how many failure are coming from your providers, gateways, etc.

After that, you can use grafrana (Port 8081 if you are using the dockerfile) and `add a new graph with your information <http://grafana.org/docs/features/graphite/>`__. The first days, you will feel lost, after a few weeks I'm sure that you will love it ;-)


.. image:: img/grafana3.png
   :alt: Grafana kamailio integration dashboard
   :align: center

If you have any trouble, you can ping me in my email, or in twitter `@eloycoto <http://twitter.com/eloycoto/>`__

You can get the source of the statsd module in github:
`https://github.com/eloycoto/statsd <https://github.com/eloycoto/statsd>`__
