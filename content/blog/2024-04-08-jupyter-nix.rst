Optimizing Python Development: Virtualenv Kernels with Nix and Jupyter
======================================================================

:date: 2024-04-08 18:00
:language: en-GB
:author: eloycoto
:head: Optimizing Python Development: Virtualenv Kernels with Nix and Jupyter
:index_title: Optimizing Python Development: Virtualenv Kernels with Nix and Jupyter
:metatitle: Optimizing Python Development: Virtualenv Kernels with Nix and Jupyter
:tags: nix, python
:metatags: python development, python, jupyter, nix
:description: Explore how to efficiently manage Python package dependencies using Nix and JupyterLab. Learn practical solutions to streamline your development workflow.
:keywords: python, nix, home-manager, jupyterlab, jupyter kernel

Over the past few weeks, I have been immersing myself in mathematics and
physics, while also exploring the latest advancements in GPU technologies and
the broader world of computing. However, working with Python packages can be a
bit challenging when your operating system and configuration are based on Nix.

JupyterLab is a nice tool. Having the ability to run code interactively is
incredibly useful, especially when working on algorithms. The most problematic
issue is installing any dependency, normally, Python projects use `pip` or
`conda`, dealing with packages in Nix can be time consuming.

Jupyter supports various kernels, so I started exploring the idea of installing
a new virtualenv kernel directly into Jupyter which I can install packages
using pip. The key issue here is around shared libraries in Python, prompting
me to create the following script.

.. code-block:: bash

    #!/bin/bash

    echo "Creating venv $1"
    VENV_FOLDER="$HOME/venvs/$1"

    if test -d "$VENV_FOLDER"; then
        echo "${VENV_FOLDER} is already created"
        nix shell github:GuillaumeDesforges/fix-python --command fix-python --venv $VENV_FOLDER
        exit 0
    fi
    echo "creating venv $1 on folder $VENV_FOLDER"
    virtualenv $VENV_FOLDER
    $VENV_FOLDER/bin/pip install ipykernel

    nix shell github:GuillaumeDesforges/fix-python --command fix-python --venv $VENV_FOLDER
    $VENV_FOLDER/bin/python -m ipykernel install --prefix=$HOME/.local/share --name "venv-$1"
    jupyter kernelspec install --user $HOME/.local/share/share/jupyter/kernels/venv-$1


The central concept:

#. Maintain all virtualenvs within a custom folder.
#. For existing venvs, focus on fixing the Python shared libraries.
#. For new virtualenv:
    #. Create a new virtualenv.
    #. Install ipykernel for Jupyter compatibility.
    #. Resolve Python shared library dependencies.
    #. Configure the kernel.
    #. Register the new kernel for user access.

Finally, while this approach may not be ideal, it has enabled me to
pragmatically test new Python libraries without investing excessive time. Once
a solution is refined and ready, I typically transition it to a custom Flake
for more robust integration and management over time.
