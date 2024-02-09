sistemas de colas basado en redis en kamailio
==============================================

:date: 2013-04-10 00:30
:head: Sistemas de colas basado en kamailio con redis.
:index_title: Kamailio redis howto
:author: eloycoto
:metatitle: Kamailio redis, sistemas de colas - Eloy Coto
:tags: kamailio, redis, python, notifications, voip, telefonia
:metatags: kamailio, redis, python, notifications, voip, telefonia
:description: kamailio redis. Un uso diferente de usar Redis desde kamailio para poder integrarlo con otras plataformas.
:keywords: kamailio, redis, python, notifications, voip, telefonia


Desde la versión
`3.2 <http://www.kamailio.org/wiki/features/new-in-3.2.x>`__
de\ `Kamailio <http://www.kamailio.org/>`__ tiene soporte para
`Redis <http://redis.io/>`__. Junto con el módulo
`memcache <http://kamailio.org/docs/modules/3.3.x/modules_k/memcached.html>`__,
se aproxima al mundo web, algo que favorece a la telefonía en los
tiempos que vivimos. :)

Antiguamente para llamar un programa externo y tener información
detallada(en tiempo real) en otro sistema te hacía falta usar el modulo
de python, xhttp,lua..Todos son muy válidos, pero la velocidad/sencillez
que aporta redis no lo aportan los otros sistemas.

Redis es una 'Database' que esta escrita en C que empezó en el 2009, y
que esta siendo usada en muchos entornos web. Por otra parte la
estructura de datos es orientada en key=>value. Por lo que los que
venimos del mundo voip la podemos asociar a la database de Asterisk.

.. figure:: img/redis.jpg
   :alt: class

Para un sistema de colas es simple. Existe un proceso(o varios) que
inserta los datos (Comando `RPUSH <http://redis.io/commands/rpush>`__) y
un proceso (worker) que esta a la espera de que el master inserte datos
(`BLPOP <http://redis.io/commands/blpop>`__) para poder ejecutar la
acción, ahora os dejo un ejemplo:

Inserción de datos (Kamailio):

Para la instalación del módulo de redis, `simplemente tenemos que seguir
esta guía de la wiki de
kamailio <http://www.kamailio.org/wiki/install/3.3.x/git>`__ cambiando
el *make FLAVOUR* por este:

::

    make FLAVOUR=kamailio include_modules="db_mysql ndb_redis" cfg

Una vez instalado deberemos hacer los siguientes cambios en el
kamailio.cfg:

::

       loadmodule "ndb_redis.so"
    modparam("ndb_redis", "server", "name=srvN;addr=127.0.0.1;port=6379;db=0")
    route{
      ...
      ...
      ...
      ...
      if(redis_cmd("srvN", "RPUSH calls $ci", "r")) {
        # success
        xlog("===== $redis(r=&gt;type) * $redis(r=&gt;value)\n");
      }
    }

Obtención de datos (python):

::

    pip install hiredis
    pip install redis

        import redis
        def queue():
            r= redis.StrictRedis(host='127.0.0.1', port=6379, db=1)
            while True:
                (queue, msg) = r.blpop('invites')
                print 'Entrada en la cola %s y con datos %s'%(queue,msg)

        if __name__ == '__main__':
            queue()

Con este módulo se me ocurren varias aplicaciones que realizar:

-  Tener el numero de llamadas que se están cursando.
-  Un sistema de colas para generar los cdrs.
-  Notificación para sistemas de prepago, descontar saldo etc..
-  Notificación de estados de llamadas en un dashboard.

Como veis la aplicación es bastante sencilla, y en sistemas que no sean
puramente de voz, viene muy bien para interaccionar con otros programas.

Dentro de poco mostraré la integración de Opensips con Mongodb. Esta
database no es que me apasione, pero lo de poder escribir objetos json,
es muy rápido para ciertos casos.
