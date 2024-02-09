Para hacerlo mal, mejor no hacerlo
===========================================

:date: 2012-11-28 12:25
:head: Para hacerlo mal mejor no hacerlo
:author: eloycoto
:metatitle: Para hacerlo mal, mejor no hacerlo
:tags: productividad, software libre, jira, bitbucket, googleapps
:metatags: productividad, software libre, jira, bitbucket, googleapps
:description: blog sobre productividad de producto
:keywords: productividad, software libre, jira, bitbucket, googleapps



Durante el tiempo que he trabajado siempre ha existido un problema, todo
el mundo quiere pagar por un taladro de primera calidad, pero nadie es
capaz de pagar por un software de primera calidad.

Esto post va a ser referido a las herramientas que se usan en todo tipo
de empresas tecnológicas. Es muy difícil que una empresa pague una
cuantía mensual por un sistema de tickets para soporte, o que
simplemente pague por un sistema de gestión de tareas, o por el IDE del
empleado.

Además empresas tecnológicas el sistema de gestión de tareas, el control
de versiones, o el sistema operativo a usar. Lo elige un director de
sistemas o el responsable de grupo lo que acarrea una tarea costosa para
el verdadero empleado (el que reporta)

Según se asume la necesidad, la primera opción siempre es el software
libre, pero muchas veces el problema es que no existen más opciones.

Siempre he intentado trabajar en lo que me gusta, y donde evidentemente
generó valor. Por eso para mi tener que pelearme con un sistema de
tareas inválido, o tener que usar un sistema operativo que no conozco
los atajos de teclado, para mi, es tirar dinero.

Ahora dejo algunos ejemplos con mis experiencias en el entorno
empresarial:

**Cliente de correo:**

Muchas de las pequeñas empresas tienen el correo gestionado con su
proveedor de hosting, o las más alocadas montan su propio servidor.

En mi anterior etapa de `Quobis <http://www.quobis.com>`__, teníamos una
suite colaborativa basada en `Novell
Groupwise <http://www.novell.com/products/groupwise/>`__. La herramienta
era potente(mucho) pero no para una empresa de 10 empleados. Además
había la obligación de usar un cliente de correo corporativo, que en
linux era bastante lento (el 80% de la plantilla lo utilizaba), tenía
una buena web, pero no era tan buena como Gmail.

El mantenimiento de licencias salía en torno a 600€ al mes (60€
empleado) y había un coste de consumo eléctrico y mantenimiento que
había que asumir. Además de prevenir las constantes caídas que teníamos.

La decisión fue el cambio a `Google
Apps <http://www.google.co.uk/intl/en_uk/enterprise/apps/business/>`__,
que además de solucionar los problemas del correo, se mataba el servidor
de xmpp, y todos podíamos usar Google Docs. Por su parte los clientes
nativos de Iphone/Android resultan más rápidos y eficaces.

Además Gmail provee un api, que cualquier software por ahí deje que te
loguees contra el, por lo que además sirve como un **fork** de ldap.

En cuanto a todos los plugins de navegador que se pueden usar a nivel
empresarial, hace que la herramienta de google apps, no tenga rival en
entornos pequeños, y me atrevería a decir en empresas grandes, pero
cuando se elevan los usuarios herramientas como Zimbra quizás no es tan
eficaz, pero válida por costes.

**Gestión de tareas:**

Esta es de las que más me cabrea, usar un sistema de tareas decente
(Jira, Youtrack, Assembla) es algo primordial. Es muy común que mucha
gente use Redmine, yo no tengo nada contra el, pero cualquiera de los
anteriormente mencionados es muy superior a la hora del uso y de la
rapidez de gestionarlo.

Además los anteriormente comentados tienen las siguientes
características:

-  Plugins para el navegador, importante para mejorar la productividad.
-  Se actualizan solos en la versión ondemand
-  Están pensados para los programadores y para managers. Para unos
   tienen APIS y para otros gráficas. :)

De esta manera es la única (Bueno, eso fuera de España) de que el
responsable de turno no venga el lunes a preguntarte como esta el
proyecto, o que tengas que enviarle los viernes los avances del mismo.

La creación de tareas con Jira es rápida si esta bien configurado, los
reportes que da son eficaces y de esta manera se mejora la productividad
de todo el mundo.

**Servidor de control de versiones:**

Aquí va al gusto, pero esta muy ligado a la gestión de tareas, el
sistema de control de versiones para la empresa es Bitbucket,por las
siguientes razones:

-  Se integra con Jira de una manera perfecta
-  La gestión de tickets es rápida y visual + La nueva interfaz ha
   mejorado muchisimo en rapidez.
-  A nivel de precios es competitivo, por 10$/mensuales tienes 10 dev
   trabajando.

En cuanto a la opción de Github, me gusta y la interfaz es mucho más
práctica que bitbucket, pero la diferencia es que licenciar por
repositorio es más complicado para la pequeña empresa que suele tener
varios repositorios privados.

En cuanto si instalar tu propio servidor para mi no es viable, la
instalación de gitlabHQ puede llevarle a una persona 8 horas, y las
actualizaciones. Contando las horas del técnico se escapan los 10$
mensuales que vale la licencia para 10 usuarios de Bitbucket. :)

Finalmente valorar el software libre debe ser nuestra primera opción,
pero las herramientas de trabajo tienen que ser las mejores, para mi hay
una diferencia enorme entre un zimbra-gmail, jira-redmine. A veces
perder mas de 10 minutos en preparar un informe porque la aplicación no
es flexible, o no se adapta, sale bastante mas caro que pagar unos 200$
por trabajador al año.

Consecuentemente en la empresa tiene que brindar el sentido común, no es
normal que un trabajador tenga un portátil que se le apaga cuando se le
calienta, o que tenga que trabajar con Eclipse y los 2 gigabytes de
memoria RAM no sean suficientes para poder compilar. Por ahorrar 200$ se
esta tirando varios días de trabajo de un empleado.

Mas me sorprende cuando en el entorno empresarial se ven muchos
teléfonos móviles de última generación/tablets, y algunos trabajadores
están trabajando en pantallas de 15”, con ordenadores Pentium 4, y con
ratones de bola. Cuando las herramientas son buenas el trabajo será
mejor, pero las buenas herramientas no suelen estar en manos de los
*curritos*.
