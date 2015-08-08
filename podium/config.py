import os
import glob
import json
import logging
from threading import Lock

from errors import MissingConfigFileError

logger = logging.getLogger(__name__)

try:
    import yaml
except ImportError:
    logger.debug("Can't import yaml, yaml config files will not be supported")

ROOT_DIR = '.'
config_lock = Lock()
config_root = None
config_files = None
environments = None
configuration = None


def load_config_files(config_dir='config'):
    global config_files, config_root
    config_files = {}
    config_root = os.path.join(ROOT_DIR, config_dir)
    dir_queue = [config_root]
    while dir_queue:
        cur_dir = dir_queue.pop()
        for filen in glob.glob(os.path.join(cur_dir, '*')):
            if os.path.isdir(filen):
                dir_queue.append(filen)
            elif filen.endswith('.json') or filen.endswith('.yaml'):
                key = os.path.relpath(filen, config_root)[:-5]
                config_files[key] = filen


def _load_file(from_file):
    if from_file not in config_files:
        raise MissingConfigFileError(config_root, from_file)
    with open(config_files[from_file], 'r') as fp:
        if filen.endswith('.json'):
            return json.load(fp)
        else:
            return yaml.load(fp)


def load_environments(from_file='environments'):
    global environments
    environments = _load_file(from_file)


def load_config():
    global configuration
    configuration = {}