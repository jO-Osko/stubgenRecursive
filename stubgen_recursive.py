import os.path
import pkgutil
import sys

import mypy.stubgen

file_dir = os.path.dirname(__file__)
parent_dir = os.path.join(file_dir, os.pardir)
if os.path.exists(os.path.join(parent_dir, '.git')):
    # We are running from a git clone.
    sys.path.insert(0, parent_dir)

try:
    package = __import__(sys.argv[1])
except ImportError:
    print("Usage: python stubgen_recursive.py <module_name>")
    exit(1)
args = []

for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__, prefix=package.__name__ + '.',
                                                      onerror=lambda x: None):
    args.append(modname)

sys.argv[1:] = args

mypy.stubgen.main()
