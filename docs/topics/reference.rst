.. _reference:

#############
``tight-cli``
#############

The ``tight-cli`` package is one of two components, which together form Tight: the toolset that helps you build event driven applications for serverless runtimes. ``tight-cli`` helps you scaffold and maintain Tight apps. This document describes the available commands exposed by ``tight-cli``. For a more thorough discussion of how to use ``tight-cli`` to create and manage your application visit the `tutorials <tutorial.html>`_.

Once `installed <installation.html>`_, you can invoke ``tight-cli`` simply by calling ``tight`` from the command line:

.. sourcecode:: bash

    $ tight

    Usage: tight [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      dynamo
      generate
      pip

******************
``tight generate``
******************

The generate group currently supports two sub-commands: ``app`` and ``function``. Use these commands to quickly scaffold your application, functions, and tests.

======================
``tight generate app``
======================

.. sourcecode:: bash

    Usage: tight generate app [OPTIONS] NAME

    Options:
      --provider TEXT  Platform providers
      --type TEXT      Provider app type
      --target TEXT    Location where app will be created.
      --help           Show this message and exit.


``tight generate app`` only currently supports the default values for ``provider`` and ``type``. Therefore, ``NAME`` is really all that is currently required. If you don't want to generate the app in the current directory, you can override the write target by specifying the ``--target`` option.

.. sourcecode:: bash

    $ tight generate app my_service
    $ cd my_service
    $ ls -la

    drwxr-xr-x  12 user  group   408B Dec 30 14:40 .
    drwxr-xr-x@ 24 user  group   816B Dec 30 14:40 ..
    -rw-r--r--   1 user  group   143B Dec 25 17:07 .gitignore
    drwxr-xr-x   8 user  group   272B Dec 23 11:22 app
    -rw-r--r--   1 user  group    76B Dec 25 16:38 app_index.py
    -rw-r--r--   1 user  group   477B Dec 30 14:40 conftest.py
    -rw-r--r--   1 user  group    56B Dec 26 02:28 env.dist.yml
    -rw-r--r--   1 user  group    60B Dec 17 18:03 requirements-vendor.txt
    -rw-r--r--   1 user  group    40B Dec 17 18:05 requirements.txt
    drwxr-xr-x   4 user  group   136B Dec 23 12:39 schemas
    drwxr-xr-x   4 user  group   136B Dec 23 11:22 tests
    -rw-r--r--   1 user  group    55B Dec 30 14:40 tight.yml


===========================
``tight generate function``
===========================

Quickly generate a function and test stubs in a Tight app.

.. sourcecode:: bash

    Usage: tight generate function [OPTIONS] NAME

    Options:
      --provider [aws]       Platform providers
      --type [lambda_proxy]  Function type
      --help                 Show this message and exit.

This command will generate a function module and will also stub integration and unit tests for the generated module:

.. sourcecode:: bash

    $ tight generate function my_controller
    ============================================= test session starts =============================================
    platform darwin -- Python 2.7.10, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
    rootdir: /Users/michael/Development/my_service, inifile:
    collected 2 items

    tests/functions/integration/my_controller/test_integration_my_controller.py .
    tests/functions/unit/my_controller/test_unit_my_controller.py .

    ========================================== 2 passed in 0.10 seconds ===========================================
    Successfully generated function and tests!

This command generates the following files and directories:

.. sourcecode:: shell

        |-app/
        |---functions/
        |-----my_controller/
        |-------handler.py
        |-tests/
        |---functions/
        |-----unit/
        |-------my_controller/
        |---------test_unit_my_controller.py
        |-----integration/
        |-------my_controller/
        |---------expectations/
        |-----------test_get_method.yml
        |---------placebos/
        |---------test_integration_my_controller.py

The contents of the generated files:

*app/functions/my_controller/handler.py*

.. sourcecode:: python

    from tight.providers.aws.clients import dynamo_db
    import tight.providers.aws.controllers.lambda_proxy_event as lambda_proxy
    db = dynamo_db.connect()

    @lambda_proxy.get
    def get_handler(*args, **kwargs):
        return {
            'statusCode': 200,
            'body': {
                'hello': 'world'
            }
        }

    @lambda_proxy.post
    def post_handler(*args, **kwargs):
        pass

    @lambda_proxy.put
    def put_handler(*args, **kwargs):
        pass

    @lambda_proxy.patch
    def patch_handler(*args, **kwargs):
        pass

    @lambda_proxy.options
    def options_handler(*args, **kwargs):
        pass

    @lambda_proxy.delete
    def delete_handler(*args, **kwargs):
        pass

*tests/functions/integration/my_controller/test_integration_my_controller.py*

.. sourcecode:: python

    import os, json
    here = os.path.dirname(os.path.realpath(__file__))
    from tight.core.test_helpers import playback, record, expected_response_body

    def test_get_method(app, dynamo_db_session):
        playback(__file__, dynamo_db_session, test_get_method.__name__)
        context = {}
        event = {
            'httpMethod': 'GET'
        }
        actual_response = app.my_controller(event, context)
        actual_response_body = json.loads(actual_response['body'])
        expected_response = expected_response_body(here, 'expectations/test_get_method.yml', actual_response)
        assert actual_response['statusCode'] == 200, 'The response statusCode is 200'
        assert actual_response_body == expected_response, 'Expected response body matches the actual response body.'


*tests/functions/integration/my_controller/expectations/test_get_method.yml*

.. sourcecode:: yaml

    body: '{"hello":"world"}'
    headers: {Access-Control-Allow-Origin: '*'}
    statusCode: 200

*tests/functions/unit/my_controller/test_unit_my_controller.py*

.. sourcecode:: python

    def test_no_boom():
        module = __import__('app.functions.my_controller.handler')
        assert module

========================
``tight generate model``
========================

Generate a `Flywheel model <http://flywheel.readthedocs.io/en/latest/topics/models/basics.html>`_ and write to ``app/models``.

.. sourcecode:: bash

    Usage: tight generate model [OPTIONS] NAME

    Options:
      --help  Show this message and exit.

Example:

.. sourcecode:: bash

    $ tight generate model account
    $ cd app/models
    $ ls
    -rw-r--r--  1 user  group   390B Dec 30 15:28 Account.py
    -rw-r--r--  1 user  group   460B Dec 23 10:46 __init__.py

The generated model:

.. sourcecode:: python

    from flywheel import Model, Field, Engine
    import os

    # DynamoDB Model
    class Account(Model):
        __metadata__ = {
            '_name': '%s-%s-accounts' % (os.environ['NAME'], os.environ['STAGE']),
            'throughput': {
                'read': 1,
                'write': 1
            }
        }

        id = Field(type=unicode, hash_key=True)

        # Constructor
        def __init__(self, id):
            self.id = id

======================
``tight generate env``
======================

This command will generate a ``env.yml`` file, merging values defined in ``env.dist.yml`` and values in the current shell environment.

.. sourcecode:: bash

    $ tight generate env
    {CI: false, NAME: my-service, STAGE: dev}

*************
``tight pip``
*************

``tight pip`` is a lightweight command that helps manage dependencies in the context of a Tight app.


=====================
``tight pip install``
=====================

.. sourcecode:: bash

    Usage: tight pip install [OPTIONS] [PACKAGE_NAME]...

    Options:
      --requirements / --no-requirements    Defaults to --no-requirements
      --requirements-file [``CWD``]         Requirements file location
      --target [``tight.yml::vendor_dir``]  Target directory.
      --help                                Show this message and exit.


Typically, after generating an app you'll want to run ``tight pip install --requirements`` from the application root directory. This will install the dependencies to the ``app/vendored`` directory and then remove the ``boto3`` and ``botocore`` packages; these libraries should not be shipped woth your app since they are provided by AWS in the default Lambda environment.

As you are developing a Tight app, you will undoubtedly need to install additional ``pip`` packages. You have two options for installing new dependencies. You can either add the dependency to ``requirements-vendor.txt`` and re-run ``tight pip install --requirements`` or you can run ``tight pip install PACKAGE_NAME``, which will install the dependencies to ``app/vendored`` and then append ``PACKAGE_NAME`` to ``requirements-vendor.txt``.

****************
``tight dynamo``
****************

One of Tight's primary goals is to make it quick and easy to scaffold RESTful APIs. To help achieve this goal, ``tight-cli`` provides a group of commands that helps you manage, run, and test interactions with DynamoDB.

==========================
``tight dynamo installdb``
==========================

Run this command to download and expand the latest stable version of DynamoDB. The downloaded tarball will be extracted to the directory ``dynamo_db``.

======================
``tight dynamo rundb``
======================

This command will run the version of DynamoDB which was downloaded via ``tight dynamo installdb``. This command runs dynamo using a shared database file which is written to ``dynamo_db/shared-local-instance.db``.

*This file is deleted on startup if it exsits.*

Additionally, this command will traverse the ``app/models`` directory and automatically generate tables for models. Models should be instances of `Flywheel models <http://flywheel.readthedocs.io/en/latest/topics/models/basics.html>`_.

Before executing this command, you should have run ``tight generate env`` or otherwise have defined ``app/env.yml``.

.. sourcecode:: bash

    $ tight dynamo rundb

    Initializing DynamoDB Local with the following configuration:
    Port:	8000
    InMemory:	false
    DbPath:	./dynamo_db
    SharedDb:	true
    shouldDelayTransientStatuses:	false
    CorsParams:	*

    This engine has the following tables [u'my-service-dev-accounts']

As demonstrated in the example above, the command will report on the tables generated from auto-discovered model classes.

===============================
``tight dynamo generateschema``
===============================

This command will generate CloudFormation compatible DynamoDB resources from `Flywheel models <http://flywheel.readthedocs.io/en/latest/topics/models/basics.html>`_.

Given the following model:

.. sourcecode:: python

    from flywheel import Model, Field, Engine
    import os

    # DynamoDB Model
    class Account(Model):
        __metadata__ = {
            '_name': '%s-%s-accounts' % (os.environ['NAME'], os.environ['STAGE']),
            'throughput': {
                'read': 1,
                'write': 1
            }
        }

        id = Field(type=unicode, hash_key=True)

        # Constructor
        def __init__(self, id):
            self.id = id

Running ``tight dynamo generateschema`` will write a YAML file to ``app/schemas/dynamo``:

.. sourcecode:: bash

    $ tight dynamo generateschema
    $ cd schemas/dynamo
    $ ls
    -rw-r--r--  1 user  group   265B Dec 30 15:55 accounts.yml

The contents of ``acounts.yml`` will be:

.. sourcecode:: yaml

    Properties:
      AttributeDefinitions:
      - {AttributeName: id, AttributeType: S}
      KeySchema:
      - {AttributeName: id, KeyType: HASH}
      ProvisionedThroughput: {ReadCapacityUnits: 1, WriteCapacityUnits: 1}
      TableName: my-service-dev-accounts
    Type: AWS::DynamoDB::Table
