Politicas de seguridad en Kamailio
=================================================

:date: 2014-04-05 12:20
:head: Excepciones de seguridad en kamailio
:index_title: Excepciones de seguridad en kamailio.
:author: eloycoto
:metatitle: How to de reglas de seguridad en kamailio
:tags: kamailio, redis, python, seguridad, ataques, voip, sip
:metatags: kamailio, redis, python, seguridad, ataques, voip, sip
:description: Una serie de funciones para poder aplicar nuestra seguridad en kamailio sin tener que asumir riesgos usando kamailio pike, redis y python.
:keywords: kamailio, python, redis, seguridad, voip, pike


El otro día a través de este `tuit de Elio Rojano <https://twitter.com/hellc2/status/448756126382034944>`__ me anime a  documentar una serie de procesos que estamos siguiendo para mantener nuestra infraestructura segura y al mismo tiempo poder mantener las excepciones para no cortar el servicio en falsos positivos.

Para securizar kamailio lo más normal es usar el `módulo pike <http://kamailio.org/docs/modules/stable/modules/pike.html>`__, teniendo un código muy parecido a este tipo::

    route[PIKE_CHECK]{
        if (src_ip == myself)
            return(1);

        if($sht(ipban=>$si)!=$null){
            xdbg("Request $rm from blocked IP - from $fu (IP:$si:$sp)\n");
            exit;
        }

        if (!pike_check_req()){
            xlog("L_ALERT","Callid $ci -- pike blocking $rm from $fu (IP:$si:$sp)");
            $sht(ipban=>$si) = 1;
            exit;
        }
    }

Pero esto según los parámetros del modelo  podemos poner más rígido o más flexible. Si le pones flexible puedes poner en riesgo tu infraestructura. Nosotros creemos que la mejor opción es ser restrictivos y añadir opciones para desbloquear.

En nuestro caso a la ruta normal de Pike hemos añadido una serie de valores que nos son útiles para añadir datos a la blacklist:

- Validar si la extensión se parece a una existente.El caso de que se registre a la extensión 140 cuando lo normal es tener extensiones 7XXX, por otro lado para extensiones con nombre vamos a usar el `método fuzzy <https://github.com/seatgeek/fuzzywuzzy>`__.
- Validar una lista blanca de IPs que siempre están validadas.
- En caso de error tenemos una cola que obtiene el valor del `reverse dns <http://stackoverflow.com/questions/2575760/python-lookup-hostname-from-ip-with-1-second-timeout>`__ de la ip origen, si no pertenece a un dominio válido no bloqueamos.

Por otra parte muchos de nuestros clientes se conectan desde ips de hoteles/starbucks/etc. Es bastante difícil de explicar que se te bloquea desde un determinado lugar por tener problemas con el registro de su sip. Básicamente hemos añadido una opción dentro del userportal, que valida la ip como usuario y añade durante una hora la ip en la whitelist. Para hacerlo tenemos la siguiente route::

    modparam("ndb_redis", "server", "name=srvN;addr=127.0.0.1;port=6379;db=0")
    route[IS_IN_WHITE_LIST]{
        if ( redis_cmd("srvN","GET white_list:$si","r") ){
            return(1);
        }else{
            return(0);
        }
    }


Desde nuestra web básicamente hacemos los siguientes comandos dentro de redis::

    redis 127.0.0.1:6379> SET white_list:{SOURCE_IP} 1
    OK
    redis 127.0.0.1:6379> EXPIRE white_list:{SOURCE_IP} 3600
    (integer) 1

Con esto de momento y teniendo muy en cuenta la información del graphite vamos intentando solucionar todos nuestros problemas. Nuestra white list es accesible desde diferentes puntos, desde la integración con la web nuestros clientes están más contentos y al mismo tiempo en cualquier momento podemos bloquear a una IP.

Por otra parte tenemos nuestro sistema de bloqueo por rates, en el momento que un cliente se dispara de rates en un momento, lo que hacemos es borrarlo de la white_list y volvemos a bloquearlo. Por otra parte estamos buscando una manera de añadir un counter con expire, para ver que una ip no hace 100 request en 5 minutos, pero esto, de momento, es una idea.

Esto, evidentemente, no es el mejor sistema de seguridad, un robot puede llegar a acceder a la url del sistema, pero bueno, al mismo tiempo intentamos que nuestros problemas no sean problemas de nuestros clientes ;-)

PS: Desde la pasada Kamailio World conference el siguiente punto será este usar los datos de `Ips de Simwood <http://mirror.simwood.com/honeypot/>`__
