trick and tips en ansible
================================

:date: 2014-06-03 12:20
:head: 6 funciones de Ansible que no conocías
:index_title: Las mejores funciones de ansible
:metatitle: Trucos en la configuración de Ansible
:tags: ansible, devops, howto, asterisk, playbook
:author: eloycoto
:metatags: ansible, deploy, tricks, condicionales
:description: Ansible es una herramienta impresionante,aqui explicamos 6 funciones muy utiles.
:keywords: ansible, playbooks, conditionals, tricks, trucos, python, asterisk

Hace aproximadamente dos años que empecé a trabajar con Ansible. Desde ese día después de usar algo de chef/puppet y darme cabezazos contra la pared (dada su complejidad), este stack se ha convertido en mi preferido, por lo sencillo que es. No es tan completo como los anteriormente comentados, pero para mis necesidades cumple perfectamente.

Durante este tiempo han sido muchas las cosas que he aprendido, de las cuales me parece bueno salientar:

**Registro de variables**

Cada tarea tiene un resultado, muchas veces creemos que no nos dan un resultado que no sea True/False. Pero muchos módulos devuelven mucha información en un objeto json. En el código fuente de los `módulos se pueden buscar que info es la que exporta <https://github.com/ansible/ansible/blob/devel/library/commands/command#L150-L160>`__. Para poder utilizarla solo debemos hacer lo siguiente en nuestro playbook::

    - command: cat /etc/hostname
      register: my_var

    - debug: msg="Hostname == {{my_var.stdout}} Command start at {{my_var.start}}"


**Condicionales**

Las condiciones es una de las partes más sencillas de Ansible. Pero lo mejor que este sistema tiene es la capacidad de hacer condicionales con expresiones de python, lo que nos permite validar en una sola línea:

- Usando variables internas de ansible::

    - include: debian.yml
      when: ansible_os_family == "Debian"

    - include: network.yml
      when: ansible_eth0.active

- Usando expresiones `string de python <https://docs.python.org/2/library/string.html>`__::

    - include: debian.yml
      when: "'Debian' in my_var.stdout"

    - include: debian.yml
      when: my_var.stdout.find("Debian") =>= 1

    - include: debian.yml
      when: my_var.stdout.lower() == 'debian'

**Debug**

Suele ser útil mostrar debug en un formato legible. La función debug es una gran desconocida pero hace justo lo que deseamos::

    - debug: msg="System {{ inventory_hostname }} with IP: {{ansible_eth0.ipv4}} is ready"

**pre_task y post_task**

Nosotros por ejemplo tenemos muchos roles en repositorios separados y usamos `git-submodules <http://git-scm.com/docs/git-submodule>`__. De esta manera compartimos muchos de los roles (Asterisk, Kamailio, Postgresql) por lo que muchas veces antes de ejecutar el rol, tenemos que ejecutar una serie de tareas propias del proyecto, para ello nuestros playbooks lucen así::

    - name: apply asterisk config
      hosts: prod
      gather_facts: yes
      user: root
      vars_files:
        - vars/prod.yml
        - vars/ha.yml
      roles:
        - asterisk
      post_task:
        - name: Add configs
          template: src=src/{{item}}.j2 dest=/etc/asterisk/{{item}}.conf mode=0444
          with_items:
            - extensions
            - sip
            - features


**Callbacks**

Personalmente esta es una de las funciones más interesantes que hay en `Ansible <http://jpmens.net/2012/09/11/watching-ansible-at-work-callbacks/>`__. Cada vez que el playbook o tarea acaba podemos definir una serie de `callbacks <https://github.com/ansible/ansible/blob/devel/plugins/callbacks/osx_say.py#L31>`__ y obtener información de la misma.Yo las suelo usar para enviar un resumen a nuestro xmpp de cuantas tareas se ejecutaron con cambios, la hora de los cambios y el resultado::


    class CallbackModule(object):
        def playbook_on_stats(self, stats):
            do_stuff()

**Test**

Una de las cosas que me falta en Ansible es una solución 100% opensource como `Tower <http://www.ansible.com/tower>`__. Tower no es caro, pero en nuestro caso, no es necesario este sistema. Una de las mejoras que hemos implementado es cada vez que se hace un push al server, Jenkins ejecuta un dry-run y ver el resultado de la siguiente manera::

    ansible-playbook -i host playbook.yml -C

Con lo que tenemos una lista de resultados que se van a ejecutar en la máquina. En el caso de que existan cambios tengo una mini APP que nos notifica que estan pendiente cambios sin aplicar.

Finalmente estas son las funciones que nunca ves en los ejemplos pero que son muy útiles a la hora de desarrollar y hacer despliegues en entornos de producción, pruebas y desarrollo. Yo tengo el 90% de mis servidores basados en Ansible y cada día que pasa estoy más alegre de utilizarlo.  ;-)
