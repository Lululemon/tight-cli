.. _generate_app:

###############
Generate An App
###############

Tight has been designed to aid in fast and repeatable development of microservices. As such, Tight provides a suite of commands that generate files and directories that are common to all projects. The very first generate command that we are going to explore is ``tight generate app``.

**************************
Generate Project Directory
**************************

Navigate to the location where you want to create your app. I like to keep my code projects in the ``Development`` directory in my home location, so I'll head that way.

.. sourcecode:: bash

    $ cd ~/Development

Now I'm going to use ``tight generate app`` to generate a new project. Simply provide a name as the command's only argument:

.. sourcecode:: bash

    $ tight generate app tight_app

Your app has been generated! To verify, you can list the contents of the ``tight_app`` directory.

.. sourcecode:: bash

    drwxr-xr-x  12 user  group   408B Jan  2 14:56 .
    drwxr-xr-x@ 24 user  group   816B Jan  2 14:56 ..
    -rw-r--r--   1 user  group   143B Dec 25 17:07 .gitignore
    drwxr-xr-x   8 user  group   272B Jan  2 14:56 app
    -rw-r--r--   1 user  group    76B Dec 25 16:38 app_index.py
    -rw-r--r--   1 user  group   476B Jan  2 14:56 conftest.py
    -rw-r--r--   1 user  group    56B Dec 26 02:28 env.dist.yml
    -rw-r--r--   1 user  group    60B Dec 17 18:03 requirements-vendor.txt
    -rw-r--r--   1 user  group    40B Dec 17 18:05 requirements.txt
    drwxr-xr-x   4 user  group   136B Dec 23 12:39 schemas
    drwxr-xr-x   4 user  group   136B Dec 23 11:22 tests
    -rw-r--r--   1 user  group    54B Jan  2 14:56 tight.yml

****************************
The Anatomy of a Default App
****************************

====
app/
====

The app directory, not surprisingly, contains your application's runtime logic. This directory organizes your application's function code along with dependencies and share libraries.

List the contents of the directory to see what was created:

.. sourcecode:: bash

    $ ls -la app

    drwxr-xr-x   8 user  group   272B Jan  2 14:56 .
    drwxr-xr-x  13 user  group   442B Jan  2 14:57 ..
    -rw-r--r--   1 user  group   339B Dec 23 11:22 __init__.py
    drwxr-xr-x   3 user  group   102B Dec 17 17:25 functions
    drwxr-xr-x   3 user  group   102B Dec 23 11:22 lib
    drwxr-xr-x   3 user  group   102B Dec 23 10:46 models
    drwxr-xr-x   3 user  group   102B Dec 23 10:46 serializers
    drwxr-xr-x   3 user  group   102B Jan  2 14:56 vendored

---------------
app/__init__.py
---------------

The ``app`` directory's ``__init__.py`` file augments the current environment so that application dependencies are discoverable for import.

The generator currently produces the following file:

.. sourcecode:: python

    import sys, os
    here = os.path.dirname(os.path.realpath(__file__))
    sys.path = [os.path.join(here, "./vendored")] + sys.path
    sys.path = [os.path.join(here, "./lib")] + sys.path
    sys.path = [os.path.join(here, "./models")] + sys.path
    sys.path = [os.path.join(here, "./serializers")] + sys.path
    sys.path = [os.path.join(here, "../")] + sys.path


These statements are what allow function code to import packages in the ``vendored``, ``lib``, ``models``, and ``serializers`` directories without having to use relative imports. If you do not wish to alter the environment's import path, the contents of this file can be removed. However, do not remove the file completely.

--------------
app/functions/
--------------

The functions directory is where your application's business logic lives. Later in the tutorial, when we start creating functions, we'll explain the naming and file conventions that should be followed within the ``functions`` directory.

For now all you need to know is that the directory is identified as a package, since it has a blank ``__init__.py`` file.

--------
app/lib/
--------

The ``lib`` directory is where you should keep modules and packages that are shared across functions but that aren't installable via pip.

-----------
app/models/
-----------

The ``models`` directory is where the domain objects that your application manipulates should be stored. Like the ``function`` directory, files placed in the ``model`` directory should conform to Tight's conventions.

Modules in this directory should define a single model and the name of the model and file should be the same.

Imagine creating an ``Account`` model:

.. sourcecode:: bash

    $  ls -la app/models
    drwxr-xr-x  4 user  group   136B Jan  2 15:27 .
    drwxr-xr-x  8 user  group   272B Jan  2 14:56 ..
    -rw-r--r--  1 user  group    80B Jan  2 15:27 Account.py
    -rw-r--r--  1 user  group   460B Dec 23 10:46 __init__.py

    $  less Account.py

    def Account(id):
        """ Account factory """
        return {
            'id': id
        }


----------------------
app/models/__init__.py
----------------------

Unlik the other directories that get created inside of ``app``, the ``__init__.py`` file inside of ``models`` is not empty. This file will loop through the files in the directory and automatically import the models that are defined. So long as the convention described above is followed, you will be able to succinctly import models into function modules.

The ``Acccount`` model defined above would be imported like so:

.. sourcecode:: python

    from Account import Account


----------------
app/serializers/
----------------

Tight encourages you maintain serialization logic separately from model modules. As such, Tight provides a location where serializers can be kept.

-------------
app/vendored/
-------------

The ``vendored`` directory is where your _application's_ ``pip`` packages are installed.


============
app_index.py
============

This is the module that is used to route Lambda events to the correct function.

.. sourcecode:: python

    from app.vendored.tight.providers.aws.lambda_app import app as app
    app.run()


The function ``tight.providers.aws.lambda_app.run`` collects functions from ``app/functions`` and sets attributes on the module for each function found. This means that when you go to configure your Lambda function within AWS, you can refer to module attributes that mirror functions:

.. sourcecode:: python

    app_index.a_function_in_your_app


This will call the ``handler`` function on the module located at ``app/functions/a_function_in_your_app/handler.py``.

===========
conftest.py
===========

``conftest.py`` provides the minimum confugration needed to run function tests. The module also imports the ``tight.core.test_helpers`` module, which exposes test fixtures and other goodies to help you start writing tests right away.

============
env.dist.yml
============

This file contains the default values for the environment variables that your application expects. You shouldn't store sensitive or environment specific values here. By default, this file specifies that the environment variables, ``CI`` and ``STAGE`` are expected:

.. sourcecode:: yml

    # Define environment variables here
    CI: False
    STAGE: dev

As your application evolves remember to update this file with new names:

.. sourcecode:: yml

    # Define environment variables here
    CI: False
    STAGE: dev
    SOME_API_KEY: <optionally provide a default value>

=======================
requirements-vendor.txt
=======================

Specify pip package dependencies, which will be installed to ``app/vendored`` by default.

================
requirements.txt
================

Specify pip package dependencies that are to be installed to the virtual environment. Typically this is where you'll define dependencies that are required for developing and testing your app.

**Dependencies specified here will not be packaged with your application artifact.**

========
schemas/
========

This directory will contain CloudFormation compatible DynamoDb schemas, which can be auto-generated from model definitions.

======
tests/
======

Tight really wants to help you develop your application test-first. It would be a tragedy and an embarrasment if Tight didn't provide you a place to store your tests. Once we stater generating functions, we'll dive deeper into the structure of this directory.

=========
tight.yml
=========

``tight.yml`` is this Tight app's configuration file. There's nothing too fancy about it and throughout the course of the tutorial, you'll rarely have to modify it. Just be aware that it exists and that it is the location from which the command line tool pulls the application name. Every time a ``tight`` command is run, this file is discovered and parsed and the values it defines are used throughout various commands.

********************
Install Dependencies
********************

Now that are application structure has been scaffolded, it's time to install our dependencies. First we'll install our virtual environment depedencies and then we'll install our application specific dependencies.

************************
Environment Dependencies
************************

Install environment dependencies just as you would for any other virtual environment.

.. sourcecode:: bash

    $ pip install -r requirements.txt

****************
App Dependencies
****************

Application dependencies are also installed via ``pip`` but we need to be sure that they get installed to the correct location so that when our application artifact is deployed, any third-party libraries that your application relies on are available. To install your application dependencies, navigate to your project root and run ``tight pip install --requirements``:

.. sourcecode:: bash

    $ tight pip install --requirements

When you run this command, you'll notice that at the very end of the run you are notified that the ``boto3`` and ``botocore`` packages have been removed from the ``app/vendored`` directory. This is because both packages are supplied by the AWS Lamba execution environment. Generally, you shouldn't include these packages in your application artifact.

**********
Conclusion
**********

By now, you have scaffolded your first Tight app and should have a basic grasp of the purpose and reason for the auto-generated files and directories.

You also learned how to install your application and virtual environment dependencies.

Continue reading to learn about how Tight helps you initialize and manage application environment variables.
