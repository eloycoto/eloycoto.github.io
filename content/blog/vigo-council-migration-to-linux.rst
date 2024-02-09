How Vigo Council migrate to Linux
=================================

:date: 2017-06-19 12:00
:language: en-GB
:head: How Vigo Council migrated to Linux
:author: eloycoto
:index_title: How Vigo Council migrate to Linux
:metatitle: How Vigo Council migrate to Linux
:tags: ubuntu, council, vigo
:metatags: linux migrations, ubuntu, fedora
:description: How a small council like Vigo can migrate to Linux? This post explain how Vigo Council migrate more than 800 workstations to Ubuntu.
:keywords: linux migrations, ubuntu, fedora, OpenOfficea


Last May I went to one of the most awesome meetups that were given in `Vigo
<https://en.wikipedia.org/wiki/Vigo>`__.  Hugo, from Vigo council IT department,
explained the process of how they migrated more than 800 workstations to Linux,
a process that was started on 2007. I am sharing some notes about his
presentation because I think it could be really useful and interesting for you
to know how they made it.

.. image:: img/concello.jpg
   :alt: Vigo council HQ
   :align: center


Firstly, let me introduce the IT part of the Vigo council. They have close to
1000 workstations, and they need to help all the citizen (around 300K).  All
the people that work in the council are public employees, so sometimes they are
not that proactive, something hey made Hugo's team be aware from the beginning
that the change would be difficult.

Over 2007, the IT department had multiple problems, all the workstations were
pretty old, all the OS has self-login activated without any central credentials
manager, workstations stored all the data, and sometimes user lost work.
Besides, the council did not have much money (Spanish financial crisis had just
started), and invest in IT was not a priority.

Due to budget problems, the first idea that they had was to start to use
OpenOffice, so that they can save money from Microsoft Office licenses. Over
three months one guy provided support around custom macros and other issues.
After these months all the people were using the OpenOffice suite. To avoid
problems they have some Workstations with Microsoft office to deal with
non-compatible files, but the small migration was made without much trouble.

The next problem was to renew around 600 workstations, with the money that they
had at that time they could only achieve 30 workstations using Windows so that
the update will take too long. After a deep thinking, they made a proof of
concept with custom workstations and Linux, with this approach they could
upgrade around 100 workstations per year. Finally, they chose the risky
solution, What brave people they are! "Afouteza" is called in Galicia :-)

.. raw:: html

    <div class="align-center" align="center">
    <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Vigo
    council have more than 800 users running on <a
    href="https://twitter.com/ubuntu">@ubuntu</a> 👏👏👏👏 <a
    href="https://t.co/InxGR9ujFJ">pic.twitter.com/InxGR9ujFJ</a></p>&mdash; Eloy
    Coto 🐠 (@eloycoto) <a
    href="https://twitter.com/eloycoto/status/860181098420207616">May 4,
    2017</a></blockquote>
    <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div>

Consequently to this change, they knew that this migration would be hard, and
people will complain, so they focused on providing more much value on Linux
than Windows, their main idea was to seduce employees to request Linux, to
achieve that, they made the following things before start:

- They created a new LDAP schema, this allows to all new users to login in any
  Linux workstations and always use the same credentials.
- All the migrated users will have a new email server, so they can use IMAP,
  with the LDAP login and Thunderbird as a client.
- They added some feature switches on the internal applications that made the
  Linux version more productive than the Windows version, as a consequence, users
  can finish their work faster on Linux.
- Login in the shared folders with the LDAP credentials.

The decision was made, all the IT department agreed, so the next step was to
start the migration with the less possible trouble. The process began with the
smallest teams; firstly,  they provided all the peripherals that were Linux
compatible (one of the hardest points at that time). Next, they got all the
users in that department and showed them the basic use (one-day training),
afterwards, they took the most proactive user in that department and gave him
three days training so that user was the mentor for the team. The following two
weeks after the migration, one member of the IT team was sitting close to them,
so if they had any question they can ask directly, also they had a proper
feedback from the users.

One of the hardest point to fix was when they users migrated to Linux; they
forgot that the things in Windows sometimes fail too, consequently, the IT
received many calls blaming Linux, but the issue was present in Windows too.
Instead of lost hope, they only fixed problems in Linux using feature switches,
but they did not found a good solution for this problem.

The first year was rough, a lot of new issues, making more mental training than
software changes but the users after a while were happy, the next five years
have continued without to much trouble. In the early months, to increase the
success rate, they need to create an audience for all employees. To begin with,
they started to write a blog in the council intranet, every month they shared
something to make the work faster using Linux, in the second year a big
percentage of the employees requested a new computer with Linux installed, they
only see good things in the Linux workstations!

Apart from user's side, they had more challenges ahead: the hardware one was
hard, at that time many scanners, printers and barcode scans were not Linux
compatible, so when they bought a new peripheral, they sent that to the next
department to migrate, so the problem was fixed.

Another fun history is around software! They started using Fedora 7, and they
were happy until the day that they need to upgrade to a new version. When they
tried, the update broke some packages, and they could not update with a simple
shell script. After a few tries, they needed something that they can update
without much trouble, at that time, Ubuntu was starting to make it famous, many
users began to use it, they gave a try, and finally, Ubuntu 10.04 was the OS
flavour for all users.

.. raw:: html

    <div class="align-center" align="center">
    <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">We
    started using Fedora 8, but the updates were painful. With Ubuntu 10.04 we can
    update versions without problems. <a
    href="https://twitter.com/hashtag/vigotech?src=hash">#vigotech</a></p>&mdash;
    Eloy Coto 🐠 (@eloycoto) <a
    href="https://twitter.com/eloycoto/status/860190636158353411">May 4,
    2017</a></blockquote>
    <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div>


The biggest problem that they found behind Ubuntu was the desktop environment,
so they started using Gnome 2, but after a while, Ubuntu chose to move to
Unity.  Furthermore, Gnome 3 was a big change from the previous version. They
made a proof of concept with Gnome 3, and users were lost, so they decided to
switch to Ubuntu Mate, that it is the default flavour that they are using now.

What about the OS updates? With more than 800 workstations they will be fun,
isn’t it? How they made updates? How do they know that all will work when the
update was applied? They created an excellent workflow, every day all the OS
checked security’s issues, but an internal software controls the software
updates/upgrades. Every day, ten workstations (from different departments) will
be updated in non-working hours, if something fails, they only had ten
co-workers with problems, this is slow, but they prevent to get a massive
outage on the council. So, each computer gets two significant updates per year.

At the moment, the council only have the minimum computers running on Windows,
due to some special requirements like CAD applications, or something similar.
However, the root is based all on Linux OS.

I am sure that one question that you have is how many people are currently
working on this, nowadays only one guy, who provide first line support to all
users, and he is the person in charge to make updates and new features. He
already mentions that they are collecting all the cultivated in the past, so
nowadays add a new feature meant to add a few lines of code in their
orchestration tool.

I learnt a lot on this meetup; I am glad to met these IT guys a few years ago,
I have learnt a lot from them! They shared that sometimes you need to deal with
persons instead computers, they made an excellent point, that when you make a
change, you need to create an audience first, and gave to the proactive people
what they want and they will pull their closer people to the success.

I am glad to share this history with you; I Hope you enjoyed it!
