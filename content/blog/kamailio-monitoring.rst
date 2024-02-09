How can I monitor my Voip Application?
=======================================

:date: 2015-07-24 16:00
:language: en-GB
:head: Kamailio monitoring with statsd, SIPCapture or Packetbeat
:index_title: Monitoring solutions for kamailio
:metatitle: How kamailio can be monitored with SIPCapture and other software
:author: eloycoto
:tags: kamailio, sip, SIPCapture, Packetbeat, statsd
:metatags: kamailio, graphite, influxdb, siphormer, beats
:description: Kamailio can be monitored with different tools, in this post we're going to explain why tool platform needs.
:keywords: kamailio monitoring, kamailio statsd, SIPCapture, Packetbeat


In the last `Kamailio World <{filename}./kamailio-world-2015.rst>`__ two of the
hot topics were `Packetbeat <https://www.elastic.co/products/beats>`__ and
`SIPCapture <http://SIPCapture.org/>`__.  Both projects announced good news
meanwhile the conference, people got excited about it.

SIPCapture released a new `version 5
<http://www.voipusersconference.org/2015/vuc544-homer-open-source-sip-capture/>`__,
huge work from `Alex <https://twitter.com/adubovikov>`__ and Lorenzo. Both worked
hard in this version. SIPCapture 5 provides the following new features:

- New captagent that allows lua scripting.
- Frontend was rewrited from scratch and now it's a full html5 app.
- New database structure, and full PostgresSQL support.
- New database backends in the panel, now you can use InfluxDB and ElasticSearch as data source.

**SIPCapture review on VUC**


.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/MtuvwgRLBUg" frameborder="0" allowfullscreen></iframe>


Secondly Packetbeat announced that `joined Elastic <http://apmdigest.com/elastic-acquires-Packetbeat>`_ and started a new branch
called `Beats <https://www.elastic.co/products/beats>`_. Packetbeat provides
an interface to monitor our application performance without pain. You can
monitor all SQL information, Redis, HTTP information and get some insights of
your application.

**Packetbeat presentation on OSDC 2015**

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/sGvfrA5FI5E" frameborder="0" allowfullscreen></iframe>


Finally, statsd module can be added in this list. This module provides some
features to monitor your business logic. If you want to deep on this, please
read the following posts:

- `Kamailio statsd installation <{filename}./kamailio-graphite.rst>`_
- `Kamailio statsd best practices <{filename}./kamailio_statsd.rst>`_
- `Statsd on python Vigo Meetup <{filename}./statsd-python-vigo.rst>`_

So three monitoring tools. Can we use only one? What is the strengths and the
weaknesses of these software? Is all valid for our platform? Yes, but these
projects fit for different situations, let me explain:

SIPCapture is an awesome tool, but it only can help with our SIP stack, I love
it and I use to work with it. You can check what happens in your calls, and
it's pretty useful in the following cases:

- In a production platform when you need to check what happens in a call.
- If you run TLS calls, you can debug without SSL keys into wireshark.
- You can monitor the MOS in realtime in your platform.

Packetbeat is to monitor your application performance. Nowadays Kamailio is
using a lot 3 party software (databases, Messages Queues, Cache system).
Monitoring errors or timeouts of those 3-party software can be done with
Packetbeat without pain.

Business/personal metrics must to be done in statsd. In statsd you can't define
what happens in a specific call or specific query, you're measuring the
percentile of the metric that you want it's correct, for example:

- Packetbeat said that your SQL queries took 14ms as average. But in kamailio
  you found a bottleneck in that query process, so you need to monitor into your
  code. You can use statsd_timer and found the bottleneck in the specified route.

- Your average reply time in SIPCapture is upper than 1 second, you need to
  found the bottleneck into your 5000 lines of code. With Statsd you can measure
  your routes one by one, so it's easy to found the problem with few lines of
  code.

- When new feature is implemented you want to know how many calls are using
  this feature. Statsd provides a one line code to measure your business
  statistics.


**UPDATE**: `As Alex point me in Twitter
<https://twitter.com/adubovikov/status/624541282862518272>`_, all the perf stats
can be displayed in SIPCapture included Packetbeat metrics and Influxdb metrics
sending by statsd. So SIPCapure it's perfect for support and operations.
**Awesome** work made by Lorenzo & Alex.

Some developers changed statsd for Logstash. My personal opinion about that is
the following:

- Logstash need to parse logs. Logs are slow and difficult to compute.
- For timing functions, you need to write more lines of code. With statsd you
  only use 2 lines of code to monitor specific lines.
- Logs can be broken easily in your config file.
- ES query language is more complicated than use SQL'ish in InluxDB.

Finally for telecoms companies all of the explained projects are useful.
SIPCapture is the swiss-knife for support teams. Packetbeat is an amazing tool
for all the operations teams and statsd is good for operations team and
marketing/business team to make decisions based on the current metrics.
