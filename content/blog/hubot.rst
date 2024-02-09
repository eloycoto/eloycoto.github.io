Integrando hubot con nuestro servicio xmpp
===========================================

:date: 2013-05-10 00:30
:head: Instalar Hubot con nuestro servidor jabber
:index_title: Integracion de hubot con XMPP
:author: eloycoto
:metatitle: Hubot integrado con el servidor Prosody o otro Jabber.
:tags: xmpp, github, productividad, hubot, asterisk, jabber
:metatags: xmpp, github, productividad, hubot, asterisk, jabber
:description: Instalar Hubot con interfaz Jabber para nuestras instalaciones realtime.
:keywords: xmpp, github, jingle, hubot, asterisk, queue, integracion, jira.

Hubot_ es uno de los productos más de moda en el panorama de empresas desarrolladoras de software Americanas. Iniciado y comandado por Github_, Hubot permite automatizar muchas tareas a través de tu chat de grupo.

La propia descripción de Hubot en la página web es la siguiente:

.. code-block:: javascript

    GitHub, Inc., wrote the first version of Hubot to automate our company chat room. Hubot knew how to deploy the site, automate a lot of tasks, and be a source of fun in the company. Eventually he grew to become a formidable force in GitHub. But he led a private, messy life. So we rewrote him.


.. image:: img/hubot.jpg
   :alt: hubot-fast-integration
   :align: center

En este caso Hubot es muy potente. Además es muy fácil extender los módulos existentes. La situación más normal es tenerlo integrado con Hipchat, o campfire. Pero pocas veces se ve integrado con XMPP. En mi empresa usamos bastante el XMPP, por lo que poder integrar esta herramienta es increíble para nosotros, no solo por los script existentes, si no también por lo que podemos generar.

Para instalar hubot lo primero que hay que hacer es tener la versión de `node <http://nodejs.org/>`_ / `coffee-script <http://coffeescript.org/>`_ correcta:

.. code-block:: bash

    # apt-get install build-essential libssl-dev git-core redis-server libexpat1-dev
    # cd /usr/src/
    # wget http://nodejs.org/dist/v0.8.17/node-v0.8.17.tar.gz
    # tar xf node-v0.8.17.tar.gz -C /usr/local/src &amp;&amp; cd /usr/local/src/node-v0.8.17
    # ./configure &amp;&amp; make &amp;&amp; make install
    # npm install -g coffee-script

Una vez instaladas todas las dependencias solamente hay que hacer el deploy del código base.


.. code-block:: bash

    # cd /opt
    # git clone git://github.com/github/hubot.git &amp;&amp; cd hubot
    # npm install

Una vez instalado tenemos que comprobar que funciona correctamente, para ello ejecutamos los siguientes comandos:

.. code-block:: bash

    root@deb-pruebas:/opt/hubot$ ./bin/hubot
    Hubot&gt; hubot ping
    Hubot&gt; PONG

Ahora tenemos que crear el bot que sera la configuración que se conecte a nuestro servidor:

.. code-block:: bash

    /opt/hubot/bin/hubot -c ./xmpp


Eso nos crea una carpeta llamada xmpp, ahora tenemos que entrar y editar las dependencias en el package.json para añadir nuestras necesidades:


.. code-block:: bash

    "dependencies": {
        "hubot": "&gt;=2.3.2",
        "hubot-scripts": "&gt;= 2.1.0",
        "optparse": "&gt;=1.0.3",
        "node-xmpp": "&gt;=0.3.2",
        "hubot-xmpp": "&gt;=0.1.0",
        "htmlparser": "&gt;=1.7.6",
        "soupselect": "&gt;=0.2.0",
        "underscore": "&gt;=1.3.3",
        "underscore.string": "&gt;=2.2.0rc"
    }


Ahora solo tenemos que instalar las dependencias con **npm install**. Una vez instaladas tenemos que configurar las env variables.  Donde le decimos a donde/como se tiene que conectar:


.. code-block:: bash

    export HUBOT_XMPP_USERNAME=hubot@deb-pruebas
    export HUBOT_XMPP_PASSWORD=hubot
    export HUBOT_XMPP_ROOMS=dev@dev-pruebas


Una vez configurado solo tenemos que ejecutarlo y empezar a jugar en nuestro chat de grupo:

.. code-block:: bash

    root@deb-pruebas:/$ /opt/hubot/xmpp/bin/hubot --adapter xmpp


En ese momento veremos que se conecta el usuario hubot a la conferencia y ya podemos empezar a usar los comandos en la sala.  Para listar todos los comandos y ver que se puede hacer solamente hay que ejecutar **hubot help**

Si necesitais mas scripts, `en este repositorio de github <https://github.com/github/hubot-scripts/>`_, existen un ciento de ellos totalmente diferentes. `Por otra parte aquí os dejo un tutorial para poder escribir vuestros propios plugins <http://net.tutsplus.com/tutorials/javascript-ajax/writing-hubot-plugins-with-coffeescript/>`_

Este es una pequeña demo de lo que se puede hacer.

.. raw:: html

    <iframe src="http://player.vimeo.com/video/57637316" width="500" height="314" frameborder="0"></iframe>


Yo lo he instalado recientemente, durante esta semana creo que voy a escribir varios módulos. Te imaginas obtener cuantas llamadas existen en vuestra plataforma, o quizás añadir/expulsar a un usuario a la cola solamente con un comando xmpp :-)


.. _Hubot: http://hubot.github.com/
.. _Github: http://github.com/
.. _hubotScripts: https://github.com/github/hubot-scripts
.. _hubotScriptHowto: http://net.tutsplus.com/tutorials/javascript-ajax/writing-hubot-plugins-with-coffeescript/

