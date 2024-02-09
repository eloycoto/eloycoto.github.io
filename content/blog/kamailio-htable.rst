Kamailio from tables to htables
===============================

:date: 2015-03-19 11:00
:language: en-GB
:head: From SQL tables to Kamailio hash tables.
:index_title: kamailio htables and postgres
:author: eloycoto
:metatitle: Snippet to work with PostgreSQL and Kamailio htables
:tags: kamailio, postgresql, htables
:metatags: Kamailio, hashtables, hstore
:description: Postgresql snippet that helps in the creation of news Kamailio htables with a few lines of SQL code.
:keywords: kamailio htables, htable, postgresql, hstore

Hash tables are one of the best features in Kamailio, but they can be a double
edged sword. Build web applications that work with the htables architecture can
be difficult.

I am using Django since a few years ago. This framework had helped me a lot with
forms, database models, fixtures, test, migrations, etc.. But when I needed to
use Django in conjunction with htables I found it painful: building forms,
fixtures and all that was not easy anymore.

PostgreSQL provides powerful solutions for this problems. One of my favourites
is HStore. With HStore we can move from Django models to Kamailio htables in
few lines of code.

.. image:: img/postgreSQL.png
   :alt: PostgreSQL logo
   :align: center

If, for example, we have the following data:

.. code-block:: sql

    CREATE TABLE "domain" (
        id bigserial PRIMARY KEY,
        name character varying(100) NOT NULL,
        limit_calls integer,
        limit_duration integer,
        statsd_prefix character varying(40) NOT NULL,
        params character varying(64) NOT NULL,
        strip integer,
        prefix character varying(16) NOT NULL
    );
    INSERT INTO domain
        ("name", "limit_calls", "limit_duration", "statsd_prefix", "params", "strip", "prefix")
    VALUES
        ('acalustra.com',10, 3600, 'acalustra', 'nomedia=yes',0,'0034'),
        ('acalustra.es',10, 3600, 'acalustraes', 'nomedia=yes',0,'0034');

In this case we have one table with a lot of domain preferences. In our
Kamailio we will only need read access, so the easy way it's to create a new
view that generates Kamailio htable format.

For that purpose we can use the following SQL query:

.. code-block:: sql

    CREATE extension hstore;
    drop view htable_domain;
    create view htable_domain as
        select
          rank() over (order by (x).key, name) as id,
          (name|| '::'|| (x).key)::varchar(64) as key_name,
          0 as key_type,
          0 as value_type,
          CASE WHEN ((x).value is not NULL) THEN (x).value::varchar(128) ELSE ''::varchar(128) END as key_value,
          0 as expires
        FROM (
            select name, each(hstore(domainPref)) as x from (
                select * from domain
            ) as domainPref)
        as htable;

This query uses a few PostgreSQL functions:

- `rank() <http://www.PostgreSQL.org/docs/9.4/static/tutorial-window.html>`__: Create a new id per row over the result.
- `hstore() <http://www.PostgreSQL.org/docs/9.4/static/HStore.html>`__: with the subquery(domainPref) creates a new dict like colum name -> value.

Now we have a new SQL view with the following information:

.. code-block:: none

    => select * from htable_domain;
     id │           key_name            │ key_type │ value_type │   key_value   │ expires
    ────┼───────────────────────────────┼──────────┼────────────┼───────────────┼─────────
      1 │ acalustra.com::id             │        0 │          0 │ 1             │       0
      2 │ acalustra.es::id              │        0 │          0 │ 2             │       0
      3 │ acalustra.com::limit_calls    │        0 │          0 │ 10            │       0
      4 │ acalustra.es::limit_calls     │        0 │          0 │ 10            │       0
      5 │ acalustra.com::limit_duration │        0 │          0 │ 3600          │       0
      6 │ acalustra.es::limit_duration  │        0 │          0 │ 3600          │       0
      7 │ acalustra.com::name           │        0 │          0 │ acalustra.com │       0
      8 │ acalustra.es::name            │        0 │          0 │ acalustra.es  │       0
      9 │ acalustra.com::params         │        0 │          0 │ nomedia=yes   │       0
     10 │ acalustra.es::params          │        0 │          0 │ nomedia=yes   │       0
     11 │ acalustra.com::prefix         │        0 │          0 │ 0034          │       0
     12 │ acalustra.es::prefix          │        0 │          0 │ 0034          │       0
     13 │ acalustra.com::statsd_prefix  │        0 │          0 │ acalustra     │       0
     14 │ acalustra.es::statsd_prefix   │        0 │          0 │ acalustraes   │       0
     15 │ acalustra.com::strip          │        0 │          0 │ 0             │       0
     16 │ acalustra.es::strip           │        0 │          0 │ 0             │       0

Now, in Kamailio we only need to set the htable parameters:

.. code-block:: c

    modparam("htable", "htable", "domainPref=>dbtable=htable_domain;")

With this piece of code, we can use this `htable
<http://kamailio.org/docs/modules/stable/modules/htable.html>`__ having our web
developers happy which will definitely increase our dev speed.
