Ansible: how to maintain multiple ssh-keys in different servers
===============================================================

:date: 2014-11-19 21:00
:language: en-GB
:head: How to deploy multiple ssh-keys to different servers
:author: eloycoto
:metatitle: Ansible deploy multiple ssh-keys to different servers
:tags: ansible, ssh, deploy, users
:index_title: How to deploy ssh keys across servers using ansible
:metatags: ansible, ssh, deploy, ansible roles
:description: Configure ssh_keys in the servers is a pain in the ass, with this code you can deployed/maintain easyly.
:keywords: ansible, deploy, ssh-keys, ansible role

In `Ansible <http://www.ansible.com>`__ is quite easy add users, pubkeys and other stuff to any server. If
you work in a organization where you have multiple servers, ssh-keys are a
swiss-knife, but they are kinda difficult to handle if you create/destroy
multiple servers every week.

Without using Ansible (or any other config management), to add or revoke access you will need to login in all
servers by hand (or by a script) and this is boring & error prone.

With Ansible, you can setup a playbook to keep this up to date, and be sure
that the users & keys are going to be present or absent depending on your needs
(and the server that we are working with). For this purpose, Ansible provides 2
different functions: `User <http://docs.ansible.com/user_module.html>`__ and `authorized_key <http://docs.ansible.com/authorized_key_module.html>`__. Let's see how to use them
in this small example `playbook.yml`:

.. code-block:: yml

  - hosts: all
    user: root
    vars:
      admin_group: 'admin'
      users:
        192.168.50.105:
          - {name: eloy, state: present}
    tasks:
      - name: Add admin group
        group: name={{admin_group}} state=present

      - name: Check users state
        user: name="{{item.name}}" state="{{item.state}}" group="{{admin_group}}"
        with_items: users[ansible_eth1.ipv4.address]

      - name: Add Pub key
        authorized_key: user="{{item.name}}"
                        key="{{ lookup('file', 'public_keys/'+item.name+'.pub') }}"
                        state="{{item.state}}"
        with_items: users[ansible_eth1.ipv4.address]
        when: item.state == "present"

      - name: Add admin group to sudo
        lineinfile: "dest=/etc/sudoers regexp='^%{{admin_group}}} ALL' line='%{{admin_group}} ALL=(ALL) NOPASSWD: ALL' state=present"


This snipped will perform 4 tasks that are easy to follow:

1. We need to create group admin in the machine for sudo purposes.
2. Per each host, we need to define the user and its state.
3. If the user is present, we need to copy the ssh pub key into the correct folder.
4. At the end, we need to allow the users on the admin group to sudo without password.

If you want to use this piece of code you will only need to add your users to
the `vars` section and their public keys to the `public_keys` folder inside the
Ansible repo.

Happy coding!
