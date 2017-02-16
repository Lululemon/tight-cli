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


from os.path import dirname, basename, isfile
import glob, importlib, sys
modules = glob.glob(dirname(__file__)+"/*.py")
module_names = [ basename(f)[:-3] for f in modules if isfile(f)]
module_names.remove('__init__')
current_module = sys.modules[__name__]
for class_name in module_names:
    model_class = getattr(importlib.import_module(class_name, package=class_name), class_name)
    setattr(current_module, class_name, model_class)

__all__ = module_names