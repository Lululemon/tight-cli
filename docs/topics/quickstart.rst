.. _quickstart:

Quickstart
##########


For a through introduction to Tight and all that it offers read through and follow the `tutorials <tutorial.html>`_. This quickstart guide is designed to show you the sequence of commands you have to run to get a new project up and running and ready for development.

Install
*******

Install ``tight-cli`` via, Git.

.. sourcecode:: bash

    $ pip install git+git://github.com/lululemon/tight-cli.git#egg=tight-cli


Generate a Tight App
********************

.. sourcecode:: bash

    $ tight generate app my_service


Install Environment Dependencies
********************************

.. sourcecode:: bash

    $ cd my_service
    $ pip install -r requirements.txt


Install Application Dependencies
********************************

.. sourcecode:: bash

    $ cd my_service
    $ tight pip install --requirements

Generate Environment File
*************************

.. sourcecode:: bash

    $ cd my_service
    $ tight generate env
    {CI: false, NAME: my-service, STAGE: dev}


Generate a Function & Tests
***************************

.. sourcecode:: bash

    $ cd my_service
    $ tight generate function my_function

    ============================================= test session starts =============================================
    platform darwin -- Python 2.7.10, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
    rootdir: /Users/michael/Development/my_service, inifile:
    collected 2 items

    tests/functions/integration/my_function/test_integration_my_function.py .
    tests/functions/unit/my_function/test_unit_my_function.py .

    ========================================== 2 passed in 0.12 seconds ===========================================
    Successfully generated function and tests!

