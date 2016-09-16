import os
import pkgutil
import shutil
import sys

import mypy.stubgen

file_dir = os.path.dirname(__file__)
parent_dir = os.path.join(file_dir, os.pardir)
if os.path.exists(os.path.join(parent_dir, '.git')):
    # We are running from a git clone.
    sys.path.insert(0, parent_dir)

package_name = sys.argv[1]

try:
    package = __import__(package_name)
except ImportError:
    print("Usage: python stubgen_recursive.py <module_name>")
    exit(1)
args = []

for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__, prefix=package.__name__ + '.',
                                                      onerror=lambda x: None):
    args.append(modname)

sys.argv[1:] = args

mypy.stubgen.main()

replace_files = False
# copy files
for root, dirs, files in os.walk(os.path.join("out", package_name)):
    for file in files:
        path_file = os.path.join(root, file)
        _, file_path = path_file.split(os.sep, 1)
        if replace_files or not os.path.isfile(file_path):
            shutil.copy2(path_file, file_path)
