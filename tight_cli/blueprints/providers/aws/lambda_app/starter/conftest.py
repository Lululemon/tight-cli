# content of conftest.py
import pytest, os, sys, importlib, yaml, json, boto3
here = os.path.dirname(os.path.realpath(__file__))
sys.path = [os.path.join(here, "app/vendored")] + sys.path

from tight.core.test_helpers import *

def pytest_sessionstart():
    os.environ['AWS_REGION'] = 'us-west-2'
    if 'CI' not in os.environ:
        os.environ['CI'] = 'False'
        os.environ['USE_LOCAL_DB'] = 'True'