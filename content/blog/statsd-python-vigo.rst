Statsd talk at Python Vigo Meetup
=================================

:date: 2015-04-16 16:00
:language: en-GB
:head: Measure all the things talk
:author: eloycoto
:index_title: Statsd and InfluxDB at Python Vigo Meetup
:metatitle: Statsd talk at Python Vigo Meetup
:tags: statsd, grafana, statistics, monitoring, influxdb
:metatags: influxdb, statsd, grafana
:description: This are the slides for the Python Vigo talk I gave. The topic was statsd, influxdb and grafana
:keywords: statsd, influxdb, analytics, measure, python Vigo, talk, docker

I had the luck to give a talk to the Python Vigo community. The topic was about
how to measure our python applications with few lines of code.

As you know I love statsd, so I spoke about statsd data types, InfluxDB database
and Grafana as dashboard.

.. raw:: html

    <script async class="speakerdeck-embed" data-id="83ac3b9b27974f39941924fc592f6fb2" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>


I wrote a few examples that are available in my Github Profile, so you only need
to do the following things to run those services in your server (Disclaimer: You
will need docker).

.. code-block:: bash

    git clone https://github.com/eloycoto/statsd-influxdb-examples
    cd statsd-influxdb-examples
    ./start.sh


After that, the following services will be listen in these ports:

- Influxdb: 8083 and 8086 (root/root)
- Grafana: 3000 (admin/admin)
- Statsd: 8125

Now you can test with the different python apps that you have in the repo.

Happy code!
