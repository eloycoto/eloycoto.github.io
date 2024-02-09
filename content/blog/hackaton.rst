Spring Hackaton London
=======================
:date: 2013-04-28 12:25
:head: Spring Hackaton Londres Abril 2013
:index_title: Hackathon en el Google Campus
:metatitle: Hackaton localizacion y twilio en el Google Campus
:author: eloycoto
:tags: openlayers,twilio, cloud-communications, programacion, emberjs, python
:metatags: openlayers,twilio, cloud-communications, programacion, emberjs, python
:description: Resumen de lo sucedido en la primera hackaton de primavera usando herramientas de geocalizacion
:keywords: geo, twilio, google campus, hackatoncentral, eloycoto, agonzalezro

26-28 de Abril en Londres, 3 hackathones en apenas 300 metros de distancia y muchas ganas de programar. En el pasado mes de octubre había estado en la #angelhack me quedo con un poco mal sabor de boca debido a que no cumplió mis expectativas a nivel de proyectos.

Este fin de semana, con la compañía de `@agonzalezroro <https://twitter.com/agonzalezroro/>`__, nos fuimos a la `hackatoncentral <http://hackathoncentral.com/>`__, que tenía una bases muy interesantes:

- Varios proveedores de `APIS que patrocinaban el evento <http://hackathoncentral.com/#schedule>`__. Siendo los más accesibles `OpenStreetMaps <http://www.openstreetmap.org/>`__, `twilio <http://www.twilio.com/>`__ o el `api de la policía de Reino unido <http://data.police.uk/api/docs/>`__
- Enfocado a aplicaciones locales, ya sean web o móvill.
- Tenía que ser freshcode
- Había `6 diferentes categorías <http://hackathoncentral.com/#prizes>`__ para optar a interesantes premios.

La idea era hacer un chat Webrtc/sip con `Kamailio <|filename|/blog/kamailio-redis.rst>`__ con localización en un mapa, pero finalmente, al presentar las API de los patrocinadores, la habían propuesto, por lo que la desechamos y empezamos a pensar en otra solución/idea.

La idea fue un sistema de localización de comisarías de policía en un mapa, y que al clickar en ella se pudiera llamar gratuitamente a la comisaría.

.. image:: img/springhackathon.png
    :width: 50%
    :align: center
    :alt: hackathon


Empezamos a programar y teníamos claro que usaríamos herramientas que no usábamos a menudo para así aprender algo nuevo,aqui os presento la lista:

- Backend: Finalmente usamos `Flask <http://flask.pocoo.org/docs/>`__, que es muy ligero y rápido de programar.
- Frontend: Finalmente nos decantamos por `emberjs <http://emberjs.com/>`__. Álex prefería backbone, pero yo había estudiado las últimas semanas este framework. Por otra parte también usamos `Openlayers <http://openlayers.org/>`__ con los `layers de bing <http://dev.openlayers.org/docs/files/OpenLayers/Layer/Bing-js.html>`__ para mostrar el mapa.
- Se hicieron una pequeños scrappers para detectar la situaciones de las comisarías de policía, algo liosa la API para usar, por lo que se hizo un pequeño script que lo pasaba a un fichero json.
- Para el deploy usamos `Heroku <http://www.heroku.com>`__ que nunca lo había usado, pese a leer sobre el a menudo. Muy grata satisfacción con la sencillez de hacer los deploys :-).
- Para realizar las llamadas usamos `Twilio <http://www.twilio.com>`__, que simplemente realizaba un click to call de vieja usanza.

.. image:: img/emberjs.jpg
    :width: 50%
    :align: center
    :alt: emberjs


Al final el resultado: para ser un par de días, y no haber pasado mucho tiempo por la noche creo que ha sido bastante aceptable, como no el codigo esta en `github <http://kcy.me/joh2>`__ y `se puede ver la aplicación online <http://kcy.me/joog>`__

Me alegra haber asistido a esta hackaton. Alex me ha enseñado muchos tips que me van a servir mucho durante mis jornadas laborales. Además por fin he probado esas tecnologías que siempre lees, pero que siempre tienes la duda de usarlas o no.

Nos vemos en la próxima hackathon, que espero que sea pronto. :-)
