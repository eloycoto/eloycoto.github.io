Asterisk 11 hangups handlers
============================================================

:date: 2014-10-22 16:00
:language: en-GB
:head: How to improve your hangups handlers in asterisk.
:metatitle: Asterisk 11, new feature hangup handlers
:tags: asterisk, dialplan, ari, hangup
:author: eloycoto
:index_title: Asterisk hangup into Gosub.
:metatags: asterisk, dialplan, gosub, hangup
:description: Asterisk 11 introduces hangups handlers, useful application to improve asterisk subroutines (Gosub)
:keywords: asterisk, subroutines, gosub, hangup


I don't know what I was doing when I read **Asterisk 11 new features**. Last week I read in the asterisk `mailing list about hangup handlers. <http://lists.digium.com/pipermail/asterisk-users/2014-October/284839.html>`__

One of the pains in large apps based on asterisk are hangups. If one customer hangups in the middle of one subroutine, you need to add h exten in all subroutines. This make the code difficult to maintain. This is a normal subroutine in asterisk application:

.. code-block:: c

    [from-outside]
    exten => _X.,1,Noop(Call from outside with callerid=${CALLERID(num)})
    same => n,Gosub(monkeys,${EXTEN},1)

    exten => h,1,Noop("Hangup in from-outside context")

    [monkeys]
    exten => _X.,1,Noop(Subroutine Monkeys)
    same => n,While(1>0)
    same => n,Playback(tt-monkeys)
    same => n,EndWhile()

    exten => h,1,Noop("Hangup into subrutine monkeys")

.. code-block:: c

    -- Executing [100@from-outside:1] NoOp("SIP/eloy-00000001", "Call from outside from eloy") in new stack
    -- Executing [100@from-outside:2] Gosub("SIP/eloy-00000001", "monkeys,100,1") in new stack
    -- Executing [100@monkeys:1] NoOp("SIP/eloy-00000001", "Subroutine Monkeys") in new stack
    -- Executing [100@monkeys:2] While("SIP/eloy-00000001", "1>0") in new stack
    -- Executing [100@monkeys:3] Playback("SIP/eloy-00000001", "tt-monkeys") in new stack
    -- <SIP/eloy-00000001> Playing 'tt-monkeys.gsm' (language 'en')
    == Spawn extension (monkeys, 100, 3) exited non-zero on 'SIP/eloy-00000001'
    -- Executing [h@monkeys:1] NoOp("SIP/eloy-00000001", ""Hangup into subrutine"") in new stack


In this case, you should take care how to use asterisk hangup handlers into subroutines. You can't share subroutines between different logics if the hangup are different. In Asterisk 11 was added hangup handler options, and this, personally, is one of the best features added in asterisk.

You can add a simple new hangup handler adding a simple set in the context:

.. code-block:: c

    same => n,Set(CHANNEL(hangup_handler_push)=hangup-handler,${EXTEN},1(args))

In this case, when user hangup, asterisk will use **hangup-handler** context, and no problems in the gosub.

.. code-block:: c

    [from-outside-hangup]

    exten => _X.,1,Noop(Call from outside from ${CALLERID(num)})
    same => n,Set(CHANNEL(hangup_handler_push)=hangup-handler,${EXTEN},1(args))
    same => n,Gosub(monkeys,${EXTEN},1)

    [monkeys]
    exten => _X.,1,Noop(Subroutine Monkeys)
    same => n,While(1>0)
    same => n,Playback(tt-monkeys)
    same => n,EndWhile()

    [hangup-handler]
    exten => _X.,1,Noop("Hangup into the handler")


.. code-block:: c

    -- Executing [100@from-outside-hangup:1] NoOp("SIP/eloy-00000006", "Call from outside from eloy") in new stack
    -- Executing [100@from-outside-hangup:2] Set("SIP/eloy-00000006", "CHANNEL(hangup_handler_push)=hangup-handler,100,1") in new stack
    -- Executing [100@from-outside-hangup:3] Gosub("SIP/eloy-00000006", "monkeys,100,1") in new stack
    -- Executing [100@monkeys:1] NoOp("SIP/eloy-00000006", "Subroutine Monkeys") in new stack
    -- Executing [100@monkeys:2] While("SIP/eloy-00000006", "1>0") in new stack
    -- Executing [100@monkeys:3] Playback("SIP/eloy-00000006", "tt-monkeys") in new stack
    -- <SIP/eloy-00000006> Playing 'tt-monkeys.gsm' (language 'en')
    == Spawn extension (monkeys, 100, 3) exited non-zero on 'SIP/eloy-00000006'
    -- SIP/eloy-00000006 Internal Gosub(hangup-handler,100,1) start
    -- Executing [100@hangup-handler:1] NoOp("SIP/eloy-00000006", ""Hangup into the handler"") in new stack
    -- Executing [100@hangup-handler:2] Return("SIP/eloy-00000006", "") in new stack
    == Spawn extension (monkeys, h, 2) exited non-zero on 'SIP/eloy-00000006'
    -- SIP/eloy-00000006 Internal Gosub(hangup-handler,100,1) complete GOSUB_RETVAL=


You can check the docs into the `Aserisk wiki <https://wiki.asterisk.org/wiki/display/AST/Hangup+Handlers>`__, more functions are available (push, pop, wipe). In the CLI you can check the hangup handlers with this command **core show hanguphandlers <chan>**

Happy coding!

