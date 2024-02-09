Acelerate your Ansible playbooks with async tasks
==================================================

:date: 2015-05-08 16:00
:language: en-GB
:head: Speed up your Ansible Playbooks
:index_title: Ansible async task
:metatitle: How to accelerate your Ansible Playbooks
:tags: ansible, async, debian, devops, deploy
:author: eloycoto
:metatags:  ansible, ansible playbooks, ansible async, ansible async with_items
:description: With Async tasks in Ansible you can run actions in background while short task are running, so you can speed-up your deploy.
:keywords: ansible, async, playbooks, devops

I'm always impressed with my friends of
`Streetlife <https://www.streetlife.com/about/team/>`__. They built a new
infrastructure based on immutable deploys. I'm surprised about how fast they are
able to build this
`AMIs <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html>`__, they can
start a new full configured server in only 6 min.

Three years ago I've started using `Ansible <http://docs.ansible.com/>`__. My
deploys **were** always up to twenty minutes, so one day I decided to achieve an
eight-min deploy. Eight min will be the time that I have to build a new server.

To get this eight minute build, I focused on the following tasks:

APT cache time:
---------------

When you have different roles in Ansible, usually you always set *update_cache*
in the apt task. This is pretty useful, but painful with different roles.

Ansible provides the
`cache_valid_time <http://docs.ansible.com/apt_module.html>`__ option. If you
enable it, Ansible will check the cache age. If cache age is less than your
value, apt-get update will be ignored.

.. code-block:: yaml

    - name: Installing useful packages
      apt:
        name: "{{ item }}"
        update_cache: yes
        cache_valid_time: 3600
      with_items:
        - htop
        - ngrep
        - vim


Async Tasks:
------------

Async tasks are in Ansible from version 1.7. It works like this: while one long
task is running, another short task can be executed.

For example, if you want to install pip dependencies and bower dependencies:
both are needed, both can run at the same time and both take few minutes.

With async tasks, tasks can be executed and forget, but this background task
can be checked later. So Ansible provides the option to get the task status in
any time.

The following example show how pip and bower dependencies will run in two new
coroutines. While the dependencies are being installed in the system, another
task will create the users (or any other task). Before the playbook is
finished, it's going to be checked if the coroutines has finished properly.

.. code-block:: yaml
    - name: pip install requirements (Coroutine #1)
      pip:
        requirements: /my_app/requirements.txt
        virtualenv: /my_app/venv
      async: 1000
      poll: 0
      register: pip_install

    - name: bower install requirements (Coroutine #2)
      bower:
        path: /my_app/frontend/
        state: latest
      async: 1000
      poll: 0
      register: bower_install

    - name: Add the users in the platform
      user:
        name: "{{item.name}}"
        shell: /bin/bash
        groups: "{{item.groups}}"
        state: "{{item.status}}"
      with_items:
        - {name: eloy, state: present, groups: admin}
        - {name: www, state: present, groups: admin}
        - {name: ftp, state: present, groups: admin}

    - name: PIP result check (Check coroutine #1)
      async_status:
        jid: "{{ pip_install.ansible_job_id }}"
      register: job_result
      until: job_result.finished
      retries: 30

    - name: Bower result check (Check coroutine #2)
      async_status:
        jid: "{{ bower_install.ansible_job_id }}"
      register: job_result
      until: job_result.finished
      retries: 30


Ansible async task and loops:
-----------------------------

When you start with Ansible, you use a lot of *with_items*. Loops are not
supported in Async tasks, but the following workaround can be used:

.. code-block:: yaml

    # vars.yml
    dependencies:
      - bison
      - gcc
      - git
      - make
      - mercurial


.. code-block:: yaml

    - name: Installing dependencies
      apt:
        name: "{{ ','.join(dependencies) }}"
        update_cache: yes
        cache_valid_time: 3600
      async: 1000
      poll: 0

Happy deploy!
