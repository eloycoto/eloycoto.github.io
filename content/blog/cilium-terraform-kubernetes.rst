Terraform recipes to test Cilium on Kubernetes
==============================================

:date: 2017-08-29 12:00
:language: en-GB
:head: Terraform recipes to test Cilium on Kubernetes
:index_title: Terraform recipes to test Cilium on Kubernetes
:metatitle: Terraform recipes to test Cilium on Kubernetes
:author: eloycoto
:tags: ubuntu, cilium, terraform, kubernetes
:metatags: bpf, ebpf, xdp, terraform, k8s, kubernetes, cni
:description: A terraform recipe to build a kunernetes cluster on Google Cloud Platform using cilium networking
:keywords: ubuntu, cilium, terraform, kubernetes


After almost five years, I left my job at `Foehn <https://www.foehn.co.uk/>`__;
I need a personal break, and I have decided early this year that late August
would be a good time for doing it.

During this break, I'll be doing open source for few months before starting to
look for a new place. I want to learn from the best software engineers, so I'll
be contributing the next two months to `Cilium project
<https://www.cilium.io/>`__.

If you don't know what is Cilium let me explain, Cilium is a software that
enables network security mainly on container related projects, like Docker,
Kuberntes or Itsio. The main difference between Cilium and other networking
solutions is that Cilium relies in a heavy way on a lot of new technology that
the kernel provides.

eBPF
----

Firstly, we need to understand what `BPF (Berkeley Packet Filter)
<https://en.wikipedia.org/wiki/Berkeley_Packet_Filter>`__ means. BPF is a Linux
kernel bytecode interpreter originally introduced to filter network packets
(tcpdump, ngrep).

A BPF program is compiled to bytecode by the `JIT
<https://en.wikipedia.org/wiki/Just-in-time_compilation>`__ compiler, it becomes
a native CPU execution, as a consequence of that, the filter performance
increases a lot.

BPF does not allow loops, so it is not Turing complete. A few years ago, an
extension to the original BPF was created: `eBPF(Enhanced BPF)
<http://www.brendangregg.com/blog/2015-05-15/ebpf-one-small-step.html>`__ adding
new data structures (hashtables, arrays), tail calls, kernel hooks, etc...
Furthermore, nowadays BPF programs can be executed in multiple kernel hooks,
like networking, kprobes or system calls.

If you want to deep more about how to load BPF programs in your kernel I
recommend `Cilium docs <http://cilium.readthedocs.io/en/latest/bpf/>`__, `Brendan
Gregg talks <http://www.brendangregg.com/index.html#Videos>`__ and `bcc project
<https://www.iovisor.org/technology/bcc>`__.

XDP
---

`XDP <https://www.iovisor.org/technology/xdp>`__ means Xpress Data Path; this
technology was introduced in the kernel to make the packet processing much
faster, so with XDP you can drop/pass packets very close to the network driver,
without getting the packet into the kernel userspace. This technology made
Facebook Load Balancers `10x faster
<https://twitter.com/tgraf__/status/854420210362851328>`__ than IPVS
deployments.

To have a simple vision of this technology, the following image from Cilium is
self-explanatory:

.. raw:: html

    <div class="align-center" align="center">
	<iframe src="//www.slideshare.net/slideshow/embed_code/key/5uvwUxYy1RjMd8?startSlide=60" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"></div>
    </div>

If you have doubts about Cilium, you should check `Thomas Graf presentations
<https://www.slideshare.net/ThomasGraf5>`_, where you can learn the kernel
technology on deep and how cilium implements it.

If you want to try Cilium, in the `usage documentation
<http://cilium.readthedocs.io/en/latest/gettingstarted/>`__ you have some
examples and a `vagrant box
<http://cilium.readthedocs.io/en/latest/gettingstarted/#getting-started-using-docker>`__
created for testing purpose. However, if you want to test it using Kubernetes,
things get a bit more complicated, you can use Minikube, but for testing
networking tunnels you need more nodes and minikube just provides one.

`I created a Terraform recipe <https://github.com/eloycoto/k8s-cilium-terraform>`__ where you can set-up a Kubernetes cluster with
Cilium-cni on Google Cloud Platform in a few minutes. To start playing with
that, you need to follow the process described in the Readme.

.. raw:: html

    <div class="align-center" align="center">
		<script type="text/javascript" src="https://asciinema.org/a/upgHBrafmBrKMMving98RQYAC.js" id="asciicast-upgHBrafmBrKMMving98RQYAC" data-speed="2" rows="10" data-theme="monokai" async></script>
    </div>



As soon that you login into the master node, you can see a few cilium daemon set
pods working. If you want to know the cilium status you can run the following
command:

.. code-block:: bash

	for cilium in $(kubectl -n kube-system get pods --selector=k8s-app=cilium --output=jsonpath={.items..metadata.name}); do
		echo "===============${cilium}==============="
		kubectl -n kube-system exec $cilium cilium status
		return
	done


This command iterate over all cilium-agents pods, after that, it executes
`cilium status` comand to know the status of the daemon set. The sample output
is the following, where you can see the list of `endpoints
<http://cilium.readthedocs.io/en/latest/concepts/#endpoints>`__ and the status
of all 3-party integrations.

.. code-block:: bash

	===============cilium-0m1gb===============

	This command iterate over all cilium-agent pods
	Allocated IPv4 addresses:
	 10.2.28.238
	 10.2.42.252
	 10.2.247.232
	Allocated IPv6 addresses:
	 f00d::ac10:2:0:1
	 f00d::ac10:2:0:ad
	 f00d::ac10:2:0:8ad6
	KVStore:            Ok   Etcd: http://172.16.0.2:9732 - (Leader) 3.1.0
	ContainerRuntime:   Ok
	Kubernetes:         Ok   OK
	Cilium:             Ok   OK

This setup is using VXLAN, a network virtualization technology that
encapsulates Layer 2 frames within layer 4 UDP packets; Cilium also supports
Geneve (If you want to deep more, you can read `this post
<https://blog.russellbryant.net/2017/05/30/ovn-geneve-vs-vxlan-does-it-matter/>`__
by Russel Bryant).  To know the list of tunnels (The list of k8s nodes) that
cilium is using, you can use the following command:

.. code-block:: bash

	for cilium in $(kubectl -n kube-system get pods --selector=k8s-app=cilium --output=jsonpath={.items..metadata.name}); do
		echo "===============${cilium}==============="
		kubectl -n kube-system exec $cilium cilium bpf tunnel list
		return
	done


This command iterate over all cilium-agent pods, after that, it executes the
command `cilium bpf tunnel list` where you can see the network assigned per each
node, and the IP address of the node. The correct output should be similar to
this:

.. code-block:: bash

	===============cilium-0m1gb===============
	f00d::ac10:4:0:0     172.16.0.4
	10.2.0.0             172.16.0.2
	f00d::ac10:5:0:0     172.16.0.5
	10.5.0.0             172.16.0.5
	10.4.0.0             172.16.0.4
	f00d::ac10:3:0:0     172.16.0.3
	10.3.0.0             172.16.0.3
	f00d::ac10:2:0:0     172.16.0.2


When you try to schedule a new service, cilium will allocate a new IP to load
balance the traffic, the list of the Load Balancers can be checked using the
command `cilium service list` on any cilium-agent pod, the sample command is
the following:

.. code-block:: bash

	for cilium in $(kubectl -n kube-system get pods --selector=k8s-app=cilium --output=jsonpath={.items..metadata.name}); do
		echo "===============${cilium}==============="
		kubectl -n kube-system exec $cilium cilium service list
		return
	done

	===============cilium-0m1gb===============
	ID   Frontend            Backend
	1    10.96.0.1:443       1 => 172.16.0.2:6443
	2    10.96.0.10:53       1 => 10.2.42.252:53
	3    10.109.204.101:80   1 => 10.3.15.138:5000
							 2 => 10.4.15.138:5000
							 3 => 10.5.114.197:5000


From here, you can follow the policy enforcement guide from the cilium docs. In
the coming months, I will share with you all the stuff I am learning.
