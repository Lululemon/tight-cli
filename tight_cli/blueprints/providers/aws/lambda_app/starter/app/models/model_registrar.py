from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from is_alive import IsAliveSchema

spec = APISpec(
    title='',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        MarshmallowPlugin(),
    ],
)

spec.definition('is_alive', schema=IsAliveSchema)
