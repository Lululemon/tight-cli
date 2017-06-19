import sys
import os
here = os.path.dirname(os.path.realpath(__file__))
sys.path = [os.path.join(here, "./vendored")] + sys.path
sys.path = [os.path.join(here, "./lib")] + sys.path
sys.path = [os.path.join(here, "./models")] + sys.path
sys.path = [os.path.join(here, "./serializers")] + sys.path
sys.path = [os.path.join(here, "../")] + sys.path
