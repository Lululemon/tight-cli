.. _tight_reference:

#########
``tight``
#########

*******************
``tight.providers``
*******************

The ``tight`` package currently supports only one provider: AWS.

======================================
``tight.providers.aws.lambda_app.app``
======================================

Use this package to create an entry point module. Typical usage is quite simple, as demonstrated in the following code example. Read on to learn about how module internals work.

.. sourcecode:: python

    from app.vendored.tight.providers.aws.lambda_app import app
    app.run()

When creating an app using ``tight-cli`` a file, *app_index.py*, will be automatically generated which will contain code like the snippet above.


.. automodule:: tight.providers.aws.lambda_app.app
    :members:
    :undoc-members:
    :show-inheritance:


*********************
``tight.core.logger``
*********************

.. automodule:: tight.core.logger
    :members:
    :undoc-members:
    :show-inheritance: