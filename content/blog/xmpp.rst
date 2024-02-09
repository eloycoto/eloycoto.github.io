Notificaciones de Github mediante XMPP.
===========================================

:date: 2013-03-15 12:25
:head: Notificaciones push desde github a nuestro IM
:metatitle: Notificaciones Xmpp desde nuestro servicio de Git
:author: eloycoto
:tags: git, github, xmpp, triggers, push
:metatags: git, github, xmpp, triggers, push
:description: How to use github para enviar mensajes a nuestro servidor de jabber
:keywords: git, github, xmpp, triggers, push

El concepto de desarrollador ha cambiado desde hace un par de años.
Antiguamente todo el mundo escribia sus programas, o se adaptaba algo de
software libre. Ahora se busca la integración de todos los servicios
mediante APIS.

Por una razón o por otra me ha tocado estar en los dos lados de una API.
En la de diseño del API de webphone, y en el consumo de las mismas.
Siempre que he tenido la oportunidad de usarlas he echado de menos la
información push. Siempre se puede arreglar con el uso de base de datos
y celery, pero bueno, no es lo mismo.

XMPP es un protocolo que se puede usar para todo, tanto como un sistema
de mesajeria corporativo, como servicio de presencia o `para desplegar
servicios soa. <http://bosqueviejo.net/2012/11/17/soa-con-xmpp/>`__

.. figure:: img/xmpp.png
   :alt: xmpp


Github tiene una lista de servicios push bastante interesante con cada
repositorio `(ademas los tiene liberados bajo software
libre) <https://github.com/github/github-services>`__, uno de ellos es
la integración con
`Jabber <https://github.com/github/github-services/blob/master/lib/services/jabber.rb>`__.
En un sistema de varios desarrolladores suele ser útil para notificar al
resto de usuarios de una nueva versión de código en el repositorio.En mi
actual empresa además parcheamos la entrada e insertamos los datos en
nuestra plataforma de tareas.

.. figure:: img/github.png
   :alt: github


Para configurar las notificaciones en un repositorio de Github solamente
tenemos que hacer lo siguiente,
`opciones/servicios/jabber <https://help.github.com/articles/post-receive-hooks>`__
y setear el usuario/conferencia que deseemos.

Leer los datos con python no es una tarea muy complicada, y aqui os dejo
un pequeño trozo de código que espera la entrada de un commit de github

.. raw:: python
   import logging

   from sleekxmpp import ClientXMPP
   from sleekxmpp.exceptions import IqError, IqTimeout


   class XMPPRead(ClientXMPP):
       def __init__(self, jid, password):
           ClientXMPP.__init__(self, jid, password)

           self.add_event_handler("session_start", self.session_start)
           self.add_event_handler("message", self.message)

       def session_start(self, event):
           self.send_presence()
           self.get_roster()

       def message(self, msg):
           do_stuff(msg)

   if __name__ == '__main__':
       logging.basicConfig(level=logging.DEBUG,
                           format='%(levelname)-8s %(message)s')
       xmpp =XMPPRead('User@dominio', 'secret')
       xmpp.connect()
       xmpp.process(block=True)


La verdad que echo de menos una lista de triggers en muchos servicios en
los que cuando ocurra una accción que se notifique mediante XMPP. Hay
librerías para todos los lenguajes y se puede reducir mucho las
peticiones REST que simplemente se hacen si existe algún cambio.
