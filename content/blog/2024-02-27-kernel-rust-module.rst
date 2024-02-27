Simplifying Rust Kernel Module Development with Nix
=====================================================

:date: 2024-02-27 18:00
:language: en-GB
:author: eloycoto
:head: Simplifying Rust Kernel Module Development with Nix
:index_title: Simplifying Rust Kernel Module Development with Nix
:metatitle: Navigating Rust Kernel Module Development with Nix
:tags: Rust, Kernel
:metatags: kernel development, Rust programming, Nix package manager, Linux kernel modules
:description: Explore how to streamline Rust kernel module development using the Nix package manager. Learn step-by-step instructions, best practices, and tips for navigating this powerful combination for efficient kernel development.
:keywords: Rust, kernel development, Nix, Linux, kernel modules, Rust programming, package management


Writing a kernel module is something "almost" straightforward, it has been in
there for years, and it's generally easy to work with. However, with the recent
addition of Rust support in the kernel, crafting Rust modules can become a bit
more challenging.

Recently, while exploring `Rust kernel
modules <https://github.com/Rust-for-Linux/rust-out-of-tree-module>`_, I found
myself in trouble to set custom flags and specialized tooling. While starting
out is still accessible, the process can be a bit slow. Typically, I rely on
building the image with `packer <https://www.packer.io/>`_ - as we `did at
Cilium <https://github.com/cilium/packer-ci-build>`_ -, but this time, I wanted
to try something new.

`Nix <https://nix.dev/>`_ is a ephimeral package manager. While I've used
Nix-shell for some validations in the past, I haven't explored all its
features. With Nix, creating a custom VM takes only a matter of minutes, making
it the perfect tool for this project.

However, starting with Nix is not easy! It has its own custom functional
language, which comes with its own learning curve. Additionally, some
definitions can be a bit tricky to work with.

Nix flake
**********

The main entry for Nix is a **flake.nix** config,which defines two primary
components: **inputs** and **outputs**. *Inputs* specify where the packages will be
located, essentially serving as the repository at its most basic level. *Outputs*
determine what we aim to build, whether it's a filename, a binary, or a virtual
machine (VM).


.. code-block:: nix

    {
      inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
      };

      outputs = inputs@{ self, nixpkgs, ... }: {
        nixosConfigurations.vm = nixpkgs.lib.nixosSystem {
          system = "x86_64-linux";
          specialArgs = { inherit inputs; };
          modules = [
            ./configuration.nix
          ];
        };
      };
    }


Here, the inputs specify our usage of the Nix `unstable repository
<https://nixos.wiki/wiki/Nix_channels>`_, while the output indicates the
construction of a new VM using the *configuration.nix* file.

Building this flake is as easy as running:

.. code-block:: bash

    nix build -L --show-trace ./#nixosConfigurations.vm.config.system.build.vm

Still, the real magic lies within the **configuration.nix** file, which resembles
to something like this:

.. code-block:: nix

    { config, pkgs, inputs, ... }:
    {
      environment.systemPackages = with pkgs; [
        git
        vim
        wget
        curl
      ];

      users.users.alice = {
        isNormalUser = true;
        extraGroups = [ "wheel" ];
        packages = with pkgs; [
          vim
        ];
        initialPassword = "test";
      };

      security.sudo.wheelNeedsPassword = false;
      services.sshd.enable = true;

      system.stateVersion = "24.05";
    }

This straightforward config file installs some essential packages like git and
vim and predefines a user named alice. Starting the VM is as simple as:

.. code-block:: bash

    QEMU_KERNEL_PARAMS=console=ttyS0 ./result/bin/run-nixos-vm -nographic; reset]

This command fires up a VM equipped with the basic tools.

Rust kernel Support
********************

For writing kernel modules in Rust, you need to follow specific guidelines:

- `Rust out of tree example <https://github.com/Rust-for-Linux/rust-out-of-tree-module>`_
- `Rust guide in the kernel doc <https://github.com/torvalds/linux/blob/45ec2f5f6ed3ec3a79ba1329ad585497cdcbe663/Documentation/rust/index.rst>`_

Additionally, you must enable certain configurations in the kernel

.. code-block:: bash

    $ zcat /proc/config.gz | grep -e "RUST[_=]"
    CONFIG_RUST_IS_AVAILABLE=y
    CONFIG_RUST=y
    CONFIG_HAVE_RUST=y
    # CONFIG_RUST_DEBUG_ASSERTIONS is not set
    CONFIG_RUST_OVERFLOW_CHECKS=y
    # CONFIG_RUST_BUILD_ASSERT_ALLOW is not set

Compiling the kernel can be time-consuming. Thankfully, Nix offers a way to use
a precompiled kernel with Rust support by adding the following config to
*configuration.nix*:


.. code-block:: nix

  boot.kernelPatches = [
    {
      name = "Rust Support";
      patch = null;
      features = { rust = true; };
    }
  ];

With Rust enabled in the kernel, the next step is building our module. Let's
delve into the `mkDerivation
<https://nixos.org/guides/nix-pills/fundamentals-of-stdenv.html#id1464>`_ from
Nix:

.. code-block:: nix

    {
      lib,
      stdenv,
      kernel,
    }:

    stdenv.mkDerivation {
      pname = "debugdriver";
      version = "1";

      src = ./src;

      nativeBuildInputs = kernel.moduleBuildDependencies;
      makeFlags = kernel.makeFlags ++ [ "KDIR=${kernel.dev}/lib/modules/${kernel.modDirVersion}/build" ];

      installFlags = [ "INSTALL_MOD_PATH=${placeholder "out"}" ];
      installTargets = [ "modules_install" ];

      meta = {
        broken = !kernel.withRust;
        description = "A basic example of rust module";
        platforms = lib.platforms.linux;
      };
    }

This configuration builds the *debugdriver* module located in the src folder.
Additionally, It's crucial to ensure that the correct patched kernel is
specified in the *configuration.nix* file.

.. code-block:: nix

  debugdriver = pkgs.callPackage ./module.nix {
    kernel = config.boot.kernelPackages.kernel;
  };

**Note** that it utilizes `config.boot.kernelPackages` instead of `pkgs.linuxPackages`,
which lacks Rust support.

Finally, we need to specify the compilation of the kernel modue, we can follow
the official Nix guide:

.. code-block:: nix

  boot.extraModulePackages = [
    debugdriver
  ];
  boot.kernelModules = [ "debugdriver" ];

After the build, we can verify that the debugdriver module is present and ready
to be used.

This approach significantly simplifies my workflow. With a custom kernel
available in a fast VM, debugging and making changes becomes a breeze without
risking my host system.

You can find my test example `here <https://github.com/eloycoto/rust-kernel-flake>`_.


Before wrapping up, I'd like to extend a special acknowledgment to `Julian
Stecklina <https://x86.lol/>`_  for the `incredible work
<https://github.com/search?q=is%3Apr%20author%3Ablitz%20&type=pullrequests>`_
he's been doing on the Nix packages. His dedication and contributions have
undoubtedly made the journey of Rust kernel module development with Nix
smoother and more enjoyable for many developers. Kudos, Julian!
