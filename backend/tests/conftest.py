import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
MANAGE_PATH = os.path.join(BASE_DIR)
project_dir_content = os.listdir(BASE_DIR)
pytest_plugins = ['tests.fixtures.fixture_user',]
