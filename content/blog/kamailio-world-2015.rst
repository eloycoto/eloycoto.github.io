Kamialio World 2015
===================

:date: 2015-06-17
:language: en-GB
:author: eloycoto
:head: My review of Kamailio World 2015
:index_title: Kamailio World 2015 review
:metatitle: Kamailio World 15 review about all the talks&annoucements.
:tags: kamailio, kamailio world
:metatags: kamailio, kamailio World, Berlin,
:description: Kamailio World was a good fun. I learnt a lot so I wrote about the best talks in the conference.
:keywords: kamailio, kamailio World, Berlin

Last week of May I had the luck to attend `Kamailio World Conference
<http://conference.kamailio.com/k03/>`__. It was my third time and as usually I
learnt a lot. **Kamailio was born fourteen years ago**, so a lot of people had a
lot of things to show.

This year the conference was focused in the following topics:

WebRTC
------

*WebRTC* is the highway to the future. HTML5 is a reality in web world nowadays.
WebRTC is supported in some browsers and only need a push from Apple and
Microsoft to reach all possible customers. Meanwhile companies like `Tuenti
<http://corporate.tuenti.com/en/dev/blog/Building-a-VoIP-Service-using-WebRTC>`__
are using WebRTC in their apps and they provide some valuable feedback to the
community.

`Tim Panton <https://www.youtube.com/watch?v=5yPtUbZcaKs>`__ explained how to
make WebRTC interact with some other HTML features. I loved the concept and I
think that WebRTC doesn't need to be another phone in the web. Innovation and
integration with the web will be the key to the success.

`Jssip <https://www.youtube.com/watch?v=cTEjYj0AUlM>`__ was explained by José
Luis Millán. I use to work with this library, so for me was not as interested
as it could be. But if you want to add some SIP-over-websocket library you
should definitely take a look to this talk.

Mobile Operators- IMS
---------------------

I'm not an expert in IMS or mobile operators, but some of the talks gave us
some insights about the IMS world. As every year I learnt a lot about IMS. This
time `3GPP-SMS-V2 kamailio module
<http://kamailio.org/docs/modules/devel/modules/smsops.html>`__ was presented
by `Carsten Bock <https://www.youtube.com/watch?v=pgYVMHVUemM>`__, and he
introduced us in the SMS solutions using Kamailio.

About mobile operators `Dragos Vingarzan
<https://www.youtube.com/watch?v=R4iu7dIdczI>`__ shows to us all the possible
solutions about open mobile networks. He explained about how to build
distributed mobile network and dived us into `OpenEPC project
<http://www.openepc.com/>`__. In case of natural disasters this project is a
fast solution for rescue teams. Well done!

Every year FhG Fokus Institute exposes all the new stuff related with mobile
network. This year `Thomas Magedanz
<https://www.youtube.com/watch?v=SZ5hjvZnmUk>`__ explained all the work that
they are doing in 5G technology.

.. image:: img/kworld-2015-daniel.jpg
   :alt: Daniel closed another great Kamaialio World
   :align: center

Pure Voip Applications
----------------------

The reason why I always go to KWorld is for Voice Apps and to learn about third
party applications that integrates with Kamailio. Last year I had seen Cgrates
and few months later I started to use it.

This year `Dan presented Cgrates LCR
<https://www.youtube.com/watch?v=Hsvcwleb-fY>`__, this technology is pretty
interesting for wholesale providers. In the other hand Matt Jordan provided us
some insights about how to `build voice apps with the new version of Asterisk
<https://www.youtube.com/watch?v=9CnrU5A2g1Q>`__. I really love the new ARI
interface and it's matches perfectly with my idea of immutable servers.

On the other hand, `Federico Cabiddu
<https://www.youtube.com/watch?v=4XIrR9bwUkM&index=23&list=PLDaEs5k2Xy-vZ_zyz989AWkz8txu7YQYY>`__
talked about the `TSILO
<http://kamailio.org/docs/modules/devel/modules/tsilo.html>`__ module, it's
gorgeous.  I think that TSILO module is too useful when your business logic is
not into your kamailio config file. I'm looking forward to use TSILO with `Evapi
module <http://kamailio.org/docs/modules/devel/modules/evapi.html>`__ and it'll
help me a lot.

Another hot topic was application monitoring. `Alexandr Dubovikov
<https://www.youtube.com/watch?v=Z5IllQMSyKY&index=8&list=PLDaEs5k2Xy-vZ_zyz989AWkz8txu7YQYY>`__
presented the new version of `SIPcapture <http://sipcapture.org/>`__. Now you
don't have any reason to don't start using it.  On the other hand, `Tudor
Golubenco
<https://www.youtube.com/watch?v=0udEXKF9nAk&index=25&list=PLDaEs5k2Xy-vZ_zyz989AWkz8txu7YQYY>`__
presented `PacketBeat <https://www.elastic.co/products/beats>`__ a software to
monitor the performance of your application.

Sipgate always shows amazing use cases, `last year they spoke
<https://www.youtube.com/watch?v=OB8F2bxtsGU>`__ about their infrastructure.
This year `Sebastian Damm gave a amazing talk
<https://www.youtube.com/watch?v=j8e0D2aOE5A&list=PLDaEs5k2Xy-vZ_zyz989AWkz8txu7YQYY&index=9>`__
about how they are providing services over IPv6. Hands-on with `lunch.sipgate.de
<https://docs.google.com/forms/d/1nnjfzVAWaqt9taCOsJcdEnlrJyxbAKVZRsUdunZGfF8/viewform>`__
too, really nice initiative.

Kazoo **is** the innovation player in Kamailio. Glad to have them onboard. They
have all the config files in `Github
<https://github.com/2600hz/kazoo-configs>`__ and you can learn a lot from them,
it's a great example! This year `Luis Azedo
<https://www.youtube.com/watch?v=ukioKekTHIg>`__ was speaking about kazoo
module that is a message queue for Kamailio. Kazoo + TSILO + EVAPI can provide
a new way to make things in Kamailio and I'm looking forward to use/write about
it.

Another talk was given by `Simon Tennant
<https://www.youtube.com/watch?v=LyZq8jZaJ7U>`__ about protocols and why some
protocols were not successful. Simon is the CEO at Buddycloud. I met BuddyCloud
early 2012 in Fosdem conference. Buddycloud is a chat/twitter service based on
XMPP and open standards. You should keep an eye on this project.

Security
---------

As often, `Olle E. Johansson <https://www.youtube.com/watch?v=NSZvMfDnLts>`__
gave one of the keynotes. He explained all the problems related with old
technology and provide advices to be more secure, revolutionary and keep the
open standards, you know `#morecrypto
<https://twitter.com/hashtag/morecrypto?src=hash>`__

`Bluebox-ng <https://github.com/jesusprubio/bluebox-ng>`__ was presented by my
friend `Sergio <https://twitter.com/s3rgiogr>`__ one of the core developers. He
explained all the possible attacks in SIP and he provided some examples + tricks
about how Bluebox can help you to keep your platform secure. He spoke about
custom scripts in Bluebox so I'll check to integrate this in our Jenkis
workflow.

The last talk was given by `Daniel
<https://www.youtube.com/watch?v=yWRQamkCtTs>`__. He spoke about some security
tips in our kamailio config files. I need to say that I don't agree 100 percent
with his point of view. I think that redis is more effective than any sql in
memory database as backend, but same approach can be used with redis in this
case.

.. raw:: html

    The last talk was given by <a
    href="https://www.youtube.com/watch?v=yWRQamkCtTs">Daniel</a>. He spoke
    about some security tips in our kamailio config files. <strike>I need to say
    that I don't agree 100 percent with his point of view. I think that redis is
    more effective than any sql in memory database as backend, but same approach
    can be used with redis in this case.</strike> I saw again this talk and I
    misunderstanding a little bit. Daniel mentioned another databases and lua
    scripts, and all mysql was only a examples.  Nowadays in my cases I'm using
    redis as cache system, so I think that for us it's more useful & simple. My
    advice you must use the backend that fit in your installation in my case
    Redis works perfect.

Finally I missed a lot of people: Carlos Ruiz from TokyApp, Torrey from Voxbone,
Anton from Quobis... active members that I always learn a lot from them. In the
other hand big thanks to all the people that were involved in this conference.
It was a blast!

.. image:: img/galician_team_kworld_2015.jpg
   :alt: Galician team at kamailio world 2015
   :align: center

Huge thanks from the people to `Quobis <http://www.quobis.com>`__ (`Sergio
<https://twitter.com/s3rgiogr>`__ and `Santi <https://twitter.com/lauskin>`__).
I spent my trip with them and it was a pleasure, thanks guys.
