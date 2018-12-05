# Copyright (c) 2017 lululemon athletica Canada inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tight.providers.aws.controllers.lambda_proxy_event as lambda_proxy

from app.models.is_alive import IsAliveSchema


@lambda_proxy.get
def get_handler(*args, **kwargs):
    schema = IsAliveSchema()
    body, errors = schema.dump({})
    return {
        'statusCode': 200,
        'body': body
    }
