import sys

if any("test" in item for item in sys.argv):
    # Load test settings if running tests or pytest command
    from .test import *
else:
    from .base import *