My thoughts about CGRates
=========================

:date: 2015-05-27 21:00
:language: en-GB
:head: My experience with CGRates
:index_title: My thoughts about CGRates
:metatitle: Thoughts about Cgrates billing system
:tags: kamailio, billing, cgrates
:author: eloycoto
:metatags: kamailio, kamevapi, cgrates, billing
:description: Cgrates is a billing platform for kamailio, freeswitch.
:keywords: kamailio, kamevapi, evapi, cgrates, billing

At `Foehn <http://www.foehn.co.uk>`__, we started to use
`CGRateS <http://cgrates.org/>`__ earlier this year, nowadays (May-2015) the
platform has rated tens of millions of calls. I want to share my experience.

I discovered CGRateS in 2014 at the `Kamailio World
Conference <http://conference.kamailio.com/k03/>`__. After a few years using
different solutions we found that CGRateS suits all our needs, so I decided  to
give it a try.

The project is written in `Golang <https://golang.org/>`__, so this was the
first challenge, it's not a bad idea to learn a bit of Golang before installing
CGRateS.

One of our uses is based on `cdr client
<https://cgrates.readthedocs.org/en/latest/cdrclient.html>`__, we have some
legacy installations where we wanted to use some CGRateS features. Every few
minutes we send csv files to the platform. This method is fast, we are billing
our daily traffic without problem. On the other hand I tested 10K calls per minute
and it is still fast.

I can recommend this option if you are starting with CGRateS.

In the last weeks, we started working with `kamailio
evapi <https://github.com/cgrates/kamevapi>`__ integration. This feature provides
a realtime rating engine in the proxy. This integration is still in test-mode
but I can recommend it well:

- Performance in CGRateS is not a problem. We tested with 3K calls per minute in
  a t2-small instance. Very good result.
- Kamailio configuration with CGRateS `is easy <https://github.com/cgrates/cgrates/blob/a2e36b6ae6273a61db2d5e3b2194cd281c105e0e/data/tutorials/kamevapi/kamailio/etc/kamailio/kamailio-cgrates.cfg>`__.
- For every call, CGRateS has a cache map of the current calls, so the timeout
  is set based on the virtual balance.
- With dialog module you can set the timeouts for these calls.


On the other hand, I love the following points:

CDRStats
--------

`This feature
<https://github.com/cgrates/cgrates/blob/a2e36b6ae6273a61db2d5e3b2194cd281c105e0e/data/tariffplans/cdrstats/CdrStats.csv>`__
provides some stats per account, tenant, time frame, call queues, etc.. This is
pretty useful, for example with time frames of 24 hours, you can easily get the
Total Cost of the calls in the last 24 hours per customer. Or the ACC (Average
Call Cost) in the last 1000 calls.


It provides the best interface that I ever seen for fraud, for example:

- When TCC in the last 24 hours is more than £XXX
- When the ACC in the last 200 calls queue are more than £2
- When the ASR(Average success ratio) is less than 20%


Derivate Charging:
------------------

In our case we have some rates for customers, this was pretty easy, but we
needed that every call bills three times. One for the cost of the customer, one
for the cost of the reseller, and a one cost with our prices. With 2 lines into
DerivedChargers.csv we can get this easily.

This is pretty useful, nowadays we have a graph with our benefits, costs, and
customer costs in one single panel.

Bundles:
--------

Bundles are a swiss knife for telecoms. The good thing about CGRates is that
you can have more than one balance per account, moreover you can have two
different balances, *monetary* or *minutes*, so you can set a destination
included in a balance in minutes, when this balance finished account will be
switching to monetary balance.

With Acions Triggers you can reset the bundle every first of the month, which
means there are no problems with the recurrent balaces.

With Action Triggers you can call a action when the balance is less than XX
minutes too. It's easy to make business logic based on minutes balances.

API
---

One of the best improvements in the new version(0.9.7) is the fact that the API
is HTTP json-rpc, so it's easy to call to the API from a simple curl request or
any other software like postman.


FixedFees
----------

Another improvement in CGRateS 0.9.7 is the *cdrlog* action. With this action
you can log into the rated_cdrs table some actions. In this case I'm using it
for the recurrent fees that the customer paid for. Rent of DDIs, number of
extensions or support fees for example.

Finally I need to say, starting with CGRateS it's not easy, but when you have a
little bit of knowledge you can get CGRateS do all the hard billing work for
you.
