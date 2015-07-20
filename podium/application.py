import logging

from flask import Flask

from errors import UnrecognizedPluginError


logger = logging.getLogger(__name__)


class Application(object):
    def __init__(self, name):
        self.name = name
        self.flask_app = None
        self.plugins = {}

    def get_app(self):
        if self.flask_app is None:
            self.flask_app = Flask(self.name)
            for plugin in self.plugins.keys():
                self._init_plugin(plugin)
        return self.flask_app

    def get_plugin(self):
        if plugin_name not in self.plugins:
            raise UnrecognizedPluginError(plugin_name)

        return self.plugins[plugin_name]['instance']

    def install(self, plugin_class, lazy=True, config={}):
        if self.flask_app:
            lazy = False

        self.plugins[plugin_class.__name__] = dict(
            instance=plugin_class() if lazy else plugin_class(self.get_app()),
            inited=False if lazy else True,
            config=config,
        )

        for k, v in self.plugins[plugin_class.__name__]['config'].items():
            setattr(self.plugins[plugin_class.__name__]['instance'], k, v)

    def _init_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            raise UnrecognizedPluginError(plugin_name)

        if self.plugins[plugin_name]['inited']:
            return

        self.plugins[plugin_name]['instance'].init_app(self.get_app())
        self.plugins[plugin_name]['inited'] = True

    def run_cli(self, argv=None):
        pass

    def run_web(self, *args, **kwargs):
        self.get_app().run(*args, **kwargs)

    def __getattr__(self, key):
        return getattr(self.get_app(), key)

    def __setattr__(self, key, value):
        return setattr(self.get_app(), key, value)
