.. _overview:


########
Overview
########

Tight is an application building toolset created and optimized for serverless runtimes. With ``tight-cli`` and ``tight`` you can quickly scaffold serverless applications that are conventional, testable by default and free of boilerplate.

**Tight currently supports AWS Lambda and the Python2.7 runtime.**

The modules provided by ``tight`` make it easy to write lambda functions that act as REST resource controllers:

.. sourcecode:: python

    from tight.providers.aws.clients import dynamo_db
    import tight.providers.aws.controllers.lambda_proxy_event as lambda_proxy

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
        event = kwargs.pop('event')
        # Process request event...
        # ...
        return {
            'statusCode': 201,
        }

    @lambda_proxy.put
    def put_handler(*args, **kwargs):
        event = kwargs.pop('event')
        return {
            'statusCode': 200,
        }

    @lambda_proxy.patch
    def patch_handler(*args, **kwargs):
        pass

    @lambda_proxy.delete
    def delete_handler(*args, **kwargs):
        pass

With the ``tight-cli`` command line tool you can scaffold services, functions with test stubs and much more!

.. image:: ../_static/generate_app.gif

.. image:: ../_static/generate_function.gif


**********
Motivation
**********

*************************************
Inspiration, Alternatives & Ecosystem
*************************************


***************
Getting Started
***************
