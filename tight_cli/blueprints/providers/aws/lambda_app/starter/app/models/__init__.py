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