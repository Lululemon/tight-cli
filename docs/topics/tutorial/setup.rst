.. _setup:

Setup
#####

To get up and running with ``tight-cli`` you'll have to install the package to a virtual environment. Fore more information about setting up and installing virtual environments, visit `virtualenv <https://virtualenv.pypa.io/en/stable/>`_.

Virtual Environment
*******************

Create a new virtual environment:

.. sourcecode:: bash

    $ mkvirtualenv my_tight_app_env

Or activate an existing environment:

.. sourcecode:: bash

    $ workon my_tight_app_env

The commands ``mkvirtualenv`` and ``workon`` are provided by `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_.


Package Installation
********************

Currently, the ``tight-cli`` package is installed via git. Once you are in your virtual environment you can install the package by issuing the following command:

.. sourcecode:: bash

    $ pip install git+git://github.com/lululemon/tight-cli.git#egg=tight-cli

You are now ready to start building a Tight app!