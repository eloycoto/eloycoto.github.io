Haciendo test con sipp sin morir en el intento
===============================================

:date: 2013-08-30 10:10
:head: Validar instalaciones de SIPP con sippy_cup
:index_title: Sippy_cup howto
:author: eloycoto
:metatitle: Validacion sencilla de sipp con sippy_cup
:tags: sip, sipp, ruby, sippy_cup, test, asterisk, asteriskTestSuite
:metatags: sip, sipp, sippy_cup, asterisk, voip
:description: Sippy_cup es una herramienta de test que utiliza sipp en backend. Hace fácil probar herramientas en la web
:keywords: sipp, sip, voip, ims, testing, asterisk, kamailio, mojolingo, bklang

En el pasado Febrero cerramos un proyecto muy importante. Dicho proyecto necesita una cantidad de test, no porque el cliente lo pidiera, si no porque el SLA que teníamos con ellos nos hacia que con cualquier cambio solo teníamos ventanas muy pequeñas de tiempo. Lo que nos hizo tener que programar todos los escenarios posibles para una validación más eficiente.

Desde ese proyecto y usando `python-sipsimple <http://sipsimpleclient.org/>`_ hice un pequeño framework, para hacer test sin ser la locura de los ficheros xml de `sipp <http://sipp.sourceforge.net/>`_. En los últimos meses estaba pensando en como poder hacer un framework libre, que pudiera ser útil para demás proyectos. Cuando tenía algo de código han salido a la luz dos proyectos muy interesantes.

El primero ha sido el que ha realizado `metaswitch <http://www.metaswitch.com/>`_, que `han liberado muchas partes de sus herramientas/productos <https://github.com/Metaswitch>`_ y tiene un `framework de test muy orientado a su plataforma. <https://github.com/Metaswitch/clearwater-live-test>`_

El framework esta bien, pero era costoso de hacer sin ser referido a Metaswitch.

Esta semana `Ben Klang <https://twitter.com/bklang>`_ ha liberado `sippy_cup <http://bklang.github.io/sippy_cup/>`_, un framework que la verdad me ha dejado muy contento. Es justo lo que estaba haciendo, por lo que a partir de ahora, usare este sistema y me `centraré en enviar pull-request <https://github.com/bklang/sippy_cup/pull/8>`_ si algo veo que se puede mejorar.

Para instalar este framework hay que seguir los siguientes pasos:

**Dependencias ruby**

.. code-block:: bash

    sudo apt-get install build-essential git --yes
    curl -L https://get.rvm.io | bash -s stable
    source ~/.rvm/scripts/rvm
    rvm autolibs enable
    rvm install 1.9.3
    rvm use 1.9.3
    gem install sippy_cup


**Instalando sipp**

.. code-block:: bash

   apt-get install libpcap-dev
   cd /tmp/
   git clone https://github.com/polysics/sipp_dynamic_pcapp_play.git
   tar -xvzf sipp-xxx.tar.gz
   cd sipp-*
   patch -p1 -i /tmp/sipp_dynamic_pcapp_play/
   autoreconf -ivf
   ./configure --with-pcap
   make
   cp sipp /usr/local/bin/



**Usando sippy_cup**

Para empezar con sippy_cup se necesita crear un fichero .yml con la siguiente estructura

.. code-block:: bash

    ---
    source: 192.168.1.114
    destination: 192.168.1.120
    max_concurrent: 10
    calls_per_second: 5
    number_of_calls: 20
    sip_user: 100
    steps:
      - invite
      - wait_for_answer
      - ack_answer
      - sleep 3
      - send_digits '3125551234'
      - sleep 5
      - send_digits '#'
      - wait_for_hangup


Una vez creado el fichero, tenemos dos opciones para correr el **sippy_cup**:
 - **-c**: Esto genera solamente el .xml y el pcap que se necesita
 - **-r**: Esto hace que el programa empieze a correr y genera el flujo de llamadas.


.. code-block:: bash

    sippy_cup -cr my_test_scenario.yml
    Compiling media to /Users/eloycotopereiro/dev/sipp/sippcup/my_test_scenario.xml...done.
    Compiling scenario to /Users/eloycotopereiro/dev/sipp/sippcup/my_test_scenario.pcap...done.
    "Preparing to run SIPp command: sudo sipp -i 192.168.1.114 -p 8836 -sf /Users/eloycotopereiro/dev/sipp/sippcup/my_test_scenario.xml -l 10 -m 20 -r 5 -s 100 192.168.1.120 > /dev/null 2>&1"
    Password:
    "Test completed successfully!"

Ahora ya tenemos nuestro servicio de testing mas sencillo de leer, y mas fácil para hacer pruebas en nuestros servicios de voip.
