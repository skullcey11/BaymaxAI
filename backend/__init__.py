import os, sys
# Ensure the project root is on PYTHONPATH so that legacy modules (indexing, query, docs) can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
