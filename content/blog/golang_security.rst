Make your Golang project more secure with a few simple tools
===============================================================

:date: 2022-11-20 21:00
:language: en
:author: eloycoto
:head: Make your Golang project more secure with a few simple tools
:index_title: Make your Golang project more secure with a few simple tools
:metatitle: Make your Golang project more secure with a few simple tools
:tags: golang, programming, security
:metatags: golang, programming
:description: A small guide how to run a few simple tools in your Golang CI to make it more secure
:keywords: golang, security, programming

Over the last few years, I have been jumping between multiple Golang projects
within different teams. These are a few tools that are not well-known by many
developers but make your code a bit more secure.

These static check tools fit nicely on your CI pipelines. Other tools validate
what your code is doing on runtime (`Tetragon
<https://github.com/cilium/tetragon>`_), and some validate that your
dependencies are what it is supposed to be (`SigStore
<https://www.sigstore.dev/>`_).

Gosec:
---------

It's a community-driven tool that does static code analysis based on Golang
AST. It prevents your application from common attacks and controls SQL
injection, decompression attacks, Insecuring connections, ENV attacks and a few
others.

You can use it manually like this:

.. code-block:: bash

    docker run --rm -w /opt/data/ \
      -v $(PWD):/opt/data/:z \
      docker.io/securego/gosec \
      -exclude-generated /opt/data/...

Or using it on GitHub Actions:

.. code-block:: yaml

    ---
    name: Security
    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]

    jobs:
      Security-Scanner:
        name: Security Scanner
        runs-on: ubuntu-latest
        steps:
          - name: Check out code
            uses: actions/checkout@v2

          - name: Run Gosec Security Scanner
            uses: securego/gosec@master
            env:
              GOFLAGS: -buildvcs=false
            with:
              args: '-exclude-generated ./...'

Semgrep:
---------

Semgrep is a broader tool and supports multiple programming languages. It has a
lot of rules that are community driven and free, and it also has some extended
rules that are only available by paying a subscription.

You can use it manually like this:

.. code-block:: bash

    $ docker run --rm -v "$(pwd):/src" \
        returntocorp/semgrep \
        semgrep --config "p/golang"

Vuln:
-----

In Golang projects, it is usual to commit the vendor packages inside the
application repository. This behaviour can add some issues if one dependency
has a CVE that the infra team may be unaware of.

Vuln is a community-driven tool that checks the dependencies that are part of
the go.mod and validates that there is no CVE in the current dependency
version; if it's any, it'll inform about the dependency.

From my perspective, this tool should run daily in our CI with a clear path to
fixing it.

You can use it manually like this:

.. code-block:: bash

	govulncheck ./...

Or using it on GitHub Actions:

.. code-block:: yaml

    name: My Workflow
    on: [push, pull_request]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - name: Running govulncheck
            uses: Templum/govulncheck-action@<version>
            with:
              go-version: 1.18
              vulncheck-version: latest
              package: ./...
              github-token: ${{ secrets.GITHUB_TOKEN }}


These are the tools that I would always add to my CI; they are free and can
save your organization from any stupid risk.
